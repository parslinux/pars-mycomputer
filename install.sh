#!/usr/bin/env bash
# ==============================================================================
# Pars My Computer - System Installation Script
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

# Check root privileges
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}[!] Root privileges required for installation.${NC}"
    echo -e "${BLUE}[*] Requesting sudo permissions...${NC}"
    exec sudo bash "$0" "$@"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}${BOLD}====================================================${NC}"
echo -e "${CYAN}${BOLD}       Pars My Computer - Installation Script       ${NC}"
echo -e "${BLUE}${BOLD}====================================================${NC}"

# 1. Package manager and dependency check
check_and_install_dependencies() {
    echo -e "${BLUE}[*] Checking system dependencies...${NC}"

    if command -v apt-get &>/dev/null; then
        DEPS=(python3 python3-gi gir1.2-gtk-3.0 gir1.2-glib-2.0 gir1.2-notify-0.7 gir1.2-pango-1.0 gvfs-fuse gettext)
        MISSING=()
        for dep in "${DEPS[@]}"; do
            if ! dpkg -s "$dep" &>/dev/null; then
                MISSING+=("$dep")
            fi
        done
        if [ ${#MISSING[@]} -gt 0 ]; then
            echo -e "${YELLOW}[!] Missing packages detected: ${MISSING[*]}${NC}"
            echo -e "${BLUE}[*] Installing dependencies with apt...${NC}"
            apt-get update -y && apt-get install -y "${MISSING[@]}"
        fi
    elif command -v pacman &>/dev/null; then
        PAC_DEPS=(python python-gobject gtk3 libnotify pango gvfs gettext)
        MISSING_PAC=()
        for pdep in "${PAC_DEPS[@]}"; do
            if ! pacman -Qi "$pdep" &>/dev/null; then
                MISSING_PAC+=("$pdep")
            fi
        done
        if [ ${#MISSING_PAC[@]} -gt 0 ]; then
            echo -e "${YELLOW}[!] Missing packages detected: ${MISSING_PAC[*]}${NC}"
            echo -e "${BLUE}[*] Installing dependencies with pacman...${NC}"
            pacman -S --needed --noconfirm "${MISSING_PAC[@]}"
        fi
    fi
}

check_and_install_dependencies

# 2. Version information
echo -e "${BLUE}[*] Checking version information...${NC}"
if [ -f "debian/changelog" ]; then
    VERSION=$(head -n 1 debian/changelog | sed -n 's/.*(\(.*\)).*/\1/p')
    if [ -n "$VERSION" ]; then
        echo "$VERSION" > "src/__version__"
        echo -e "${GREEN}[+] Detected version: $VERSION${NC}"
    fi
fi
if [ ! -f "src/__version__" ]; then
    echo "0.1.0" > "src/__version__"
fi

# 3. Compile and install translation files (.mo)
echo -e "${BLUE}[*] Compiling translation catalogs...${NC}"
if command -v msgfmt &>/dev/null; then
    for po_file in po/*.po; do
        if [ -f "$po_file" ]; then
            lang=$(basename "$po_file" .po)
            target_locale_dir="/usr/share/locale/$lang/LC_MESSAGES"
            mkdir -p "$target_locale_dir"
            msgfmt "$po_file" -o "$target_locale_dir/pars-mycomputer.mo"
            echo -e "    - Installed translation: $lang ($target_locale_dir/pars-mycomputer.mo)"
        fi
    done
else
    echo -e "${YELLOW}[!] Warning: 'msgfmt' (gettext) not found. Translations skipped.${NC}"
fi

# 4. Copy application files to system directories
echo -e "${BLUE}[*] Installing application files...${NC}"

PARS_SHARE_DIR="/usr/share/pars/pars-mycomputer"
mkdir -p "$PARS_SHARE_DIR"
mkdir -p "$PARS_SHARE_DIR/src"
mkdir -p "$PARS_SHARE_DIR/ui"
mkdir -p "$PARS_SHARE_DIR/css"
mkdir -p "$PARS_SHARE_DIR/autostart"

# Copy source, UI, styles, and autostart script
cp -r src/* "$PARS_SHARE_DIR/src/"
cp -r ui/* "$PARS_SHARE_DIR/ui/"
cp -r css/* "$PARS_SHARE_DIR/css/"
cp -r autostart/pars-mycomputer-add-to-desktop "$PARS_SHARE_DIR/autostart/"
chmod +x "$PARS_SHARE_DIR/autostart/pars-mycomputer-add-to-desktop"
cp pars-mycomputer.svg "$PARS_SHARE_DIR/"

# Executable launcher (/usr/bin/pars-mycomputer)
cp pars-mycomputer /usr/bin/pars-mycomputer
chmod +x /usr/bin/pars-mycomputer

# Desktop entry
mkdir -p /usr/share/applications
cp tr.org.pars.mycomputer.desktop /usr/share/applications/

# Polkit policy
mkdir -p /usr/share/polkit-1/actions
cp tr.org.pars.pkexec.pars-mycomputer.policy /usr/share/polkit-1/actions/

# Autostart desktop entry
mkdir -p /etc/xdg/autostart
cp autostart/pars-mycomputer-add-to-desktop.desktop /etc/xdg/autostart/

# Icons
ICON_DIR="/usr/share/icons/hicolor/scalable/apps"
mkdir -p "$ICON_DIR"
cp pars-mycomputer.svg "$ICON_DIR/"
cp pars-mycomputer-emblem-pars-symbolic.svg "$ICON_DIR/"

# Optional Python setup.py registration
if [ -f "setup.py" ]; then
    python3 setup.py install --prefix=/usr --root=/ --optimize=1 &>/dev/null || true
fi

# 5. Update system caches
echo -e "${BLUE}[*] Updating system caches...${NC}"
if command -v gtk-update-icon-cache &>/dev/null; then
    gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true
fi
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database -q /usr/share/applications 2>/dev/null || true
fi

echo -e "\n${GREEN}${BOLD}====================================================${NC}"
echo -e "${GREEN}${BOLD}   [✓] Pars My Computer Successfully Installed!     ${NC}"
echo -e "${GREEN}${BOLD}====================================================${NC}"
echo -e "${CYAN}To run the application:${NC}"
echo -e "  1) From Terminal:        ${BOLD}pars-mycomputer${NC}"
echo -e "  2) From Application Menu: ${BOLD}System -> Pars My Computer${NC}\n"
