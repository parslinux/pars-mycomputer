#!/usr/bin/env bash
# ==============================================================================
# Pars My Computer - Packaging Script (Arch, Debian, Source Tarball)
# ==============================================================================

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DIST_DIR="$SCRIPT_DIR/dist"
mkdir -p "$DIST_DIR"

# Detect version
VERSION="0.8.2"
if [ -f "debian/changelog" ]; then
    VERSION=$(head -n 1 debian/changelog | sed -n 's/.*(\(.*\)).*/\1/p' || echo "0.8.2")
fi
echo "$VERSION" > "src/__version__"

echo -e "${BLUE}${BOLD}====================================================${NC}"
echo -e "${CYAN}${BOLD}       Pars My Computer - Package Builder           ${NC}"
echo -e "${BLUE}${BOLD}====================================================${NC}"
echo -e "${BLUE}[*] Package Version:${NC} $VERSION"
echo -e "${BLUE}[*] Output Directory:${NC} $DIST_DIR\n"

# Helper: compile translations locally
compile_translations() {
    echo -e "${BLUE}[*] Compiling translation catalogs...${NC}"
    if command -v msgfmt &>/dev/null; then
        for po in po/*.po; do
            [ -f "$po" ] || continue
            lang=$(basename "$po" .po)
            mkdir -p "po/$lang/LC_MESSAGES"
            msgfmt "$po" -o "po/$lang/LC_MESSAGES/pars-mycomputer.mo" 2>/dev/null || true
        done
    fi
}

# 1. Build Arch Linux Package (.pkg.tar.zst)
build_arch() {
    echo -e "${CYAN}${BOLD}>>> Building Arch Linux Package (.pkg.tar.zst)...${NC}"
    if ! command -v makepkg &>/dev/null; then
        echo -e "${YELLOW}[!] 'makepkg' not found on this system. Skipping Arch package.${NC}"
        return 1
    fi

    compile_translations
    rm -rf pkg/
    makepkg -f --nodeps

    # Move generated packages to dist/
    mv -f pars-mycomputer-*.pkg.tar.zst "$DIST_DIR/" 2>/dev/null || true
    rm -rf pkg/

    echo -e "${GREEN}[✓] Arch Linux package created in dist/${NC}\n"
}

# 2. Build Debian / Pardus / Ubuntu Package (.deb)
build_deb() {
    echo -e "${CYAN}${BOLD}>>> Building Debian / Ubuntu Package (.deb)...${NC}"
    compile_translations

    TEMP_BUILD=$(mktemp -d /tmp/pars-deb-build-XXXXXX)
    PKG_ROOT="$TEMP_BUILD/root"
    mkdir -p "$PKG_ROOT"

    # Assemble package directory layout
    mkdir -p "$PKG_ROOT/usr/bin"
    cp pars-mycomputer "$PKG_ROOT/usr/bin/"
    chmod +x "$PKG_ROOT/usr/bin/pars-mycomputer"

    mkdir -p "$PKG_ROOT/usr/share/pars/pars-mycomputer"
    cp -r src ui css "$PKG_ROOT/usr/share/pars/pars-mycomputer/"
    cp pars-mycomputer.svg "$PKG_ROOT/usr/share/pars/pars-mycomputer/"

    mkdir -p "$PKG_ROOT/usr/share/pars/pars-mycomputer/autostart"
    cp autostart/pars-mycomputer-add-to-desktop "$PKG_ROOT/usr/share/pars/pars-mycomputer/autostart/"
    chmod +x "$PKG_ROOT/usr/share/pars/pars-mycomputer/autostart/pars-mycomputer-add-to-desktop"

    mkdir -p "$PKG_ROOT/usr/share/applications"
    cp tr.org.pars.mycomputer.desktop "$PKG_ROOT/usr/share/applications/"

    mkdir -p "$PKG_ROOT/usr/share/polkit-1/actions"
    cp tr.org.pars.pkexec.pars-mycomputer.policy "$PKG_ROOT/usr/share/polkit-1/actions/"

    mkdir -p "$PKG_ROOT/etc/xdg/autostart"
    cp autostart/pars-mycomputer-add-to-desktop.desktop "$PKG_ROOT/etc/xdg/autostart/"

    mkdir -p "$PKG_ROOT/usr/share/icons/hicolor/scalable/apps"
    cp pars-mycomputer*.svg "$PKG_ROOT/usr/share/icons/hicolor/scalable/apps/"

    # Locales
    for po in po/*.po; do
        [ -f "$po" ] || continue
        lang=$(basename "$po" .po)
        mkdir -p "$PKG_ROOT/usr/share/locale/$lang/LC_MESSAGES"
        if [ -f "po/$lang/LC_MESSAGES/pars-mycomputer.mo" ]; then
            cp "po/$lang/LC_MESSAGES/pars-mycomputer.mo" "$PKG_ROOT/usr/share/locale/$lang/LC_MESSAGES/"
        elif command -v msgfmt &>/dev/null; then
            msgfmt "$po" -o "$PKG_ROOT/usr/share/locale/$lang/LC_MESSAGES/pars-mycomputer.mo"
        fi
    done

    # Debian control directory
    mkdir -p "$PKG_ROOT/DEBIAN"
    cat <<EOF > "$PKG_ROOT/DEBIAN/control"
Package: pars-mycomputer
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Maintainer: Pars Linux Topluluğu <https://github.com/parslinux>
Depends: python3, python3-gi, gir1.2-gtk-3.0, gir1.2-glib-2.0, gir1.2-notify-0.7, gir1.2-pango-1.0
Recommends: gvfs-fuse
Description: Pars My Computer - UI for disk information and management
 My Computer, modern user interface for disk information and management.
EOF

    cat <<'EOF' > "$PKG_ROOT/DEBIAN/postinst"
#!/bin/sh
set -e
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true
fi
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database -q /usr/share/applications 2>/dev/null || true
fi
exit 0
EOF
    chmod 755 "$PKG_ROOT/DEBIAN/postinst"

    DEB_NAME="pars-mycomputer_${VERSION}_all.deb"

    if command -v dpkg-deb &>/dev/null; then
        dpkg-deb --build --root-owner-group "$PKG_ROOT" "$DIST_DIR/$DEB_NAME"
    else
        # Fallback to universal ar package creation
        (
            echo "2.0" > "$TEMP_BUILD/debian-binary"
            tar -czf "$TEMP_BUILD/control.tar.gz" -C "$PKG_ROOT/DEBIAN" .
            rm -rf "$PKG_ROOT/DEBIAN"
            tar -czf "$TEMP_BUILD/data.tar.gz" -C "$PKG_ROOT" .
            cd "$TEMP_BUILD"
            ar rcs "$DIST_DIR/$DEB_NAME" debian-binary control.tar.gz data.tar.gz
        )
    fi

    rm -rf "$TEMP_BUILD"
    echo -e "${GREEN}[✓] Debian package created: dist/$DEB_NAME${NC}\n"
}

# 3. Build Source Tarball (.tar.gz)
build_tar() {
    echo -e "${CYAN}${BOLD}>>> Building Source Tarball (.tar.gz)...${NC}"
    TAR_NAME="pars-mycomputer-$VERSION.tar.gz"
    
    tar --exclude-vcs \
        --exclude='dist' \
        --exclude='pkg' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='*.pkg.tar.*' \
        --exclude='*.deb' \
        --transform="s,^,pars-mycomputer-$VERSION/," \
        -czf "$DIST_DIR/$TAR_NAME" \
        .

    echo -e "${GREEN}[✓] Source tarball created: dist/$TAR_NAME${NC}\n"
}

# Target selection
TARGET="${1:-auto}"

case "$TARGET" in
    arch)
        build_arch
        ;;
    deb)
        build_deb
        ;;
    tar)
        build_tar
        ;;
    all)
        build_tar
        build_arch || true
        build_deb
        ;;
    auto)
        build_tar
        if command -v pacman &>/dev/null || [ -f "/etc/arch-release" ]; then
            build_arch || true
        fi
        if command -v dpkg &>/dev/null || [ -f "/etc/debian_version" ]; then
            build_deb
        elif ! command -v makepkg &>/dev/null; then
            build_deb
        fi
        ;;
    *)
        echo -e "${RED}[X] Unknown target: $TARGET${NC}"
        echo -e "Usage: $0 [arch|deb|tar|all]"
        exit 1
        ;;
esac

# Summary
echo -e "${BLUE}${BOLD}====================================================${NC}"
echo -e "${GREEN}${BOLD}           Packaging Complete!                      ${NC}"
echo -e "${BLUE}${BOLD}====================================================${NC}"
ls -lh "$DIST_DIR"

echo -e "\n${BLUE}[*] SHA256 Checksums:${NC}"
(cd "$DIST_DIR" && sha256sum * 2>/dev/null || true)
echo ""
