#!/usr/bin/env bash
# ==============================================================================
# Pars My Computer - Run Application from Source
# ==============================================================================

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}${BOLD}====================================================${NC}"
echo -e "${CYAN}${BOLD}       Pars My Computer (pars-mycomputer)           ${NC}"
echo -e "${BLUE}${BOLD}====================================================${NC}"
echo -e "${BLUE}[*] Working directory:${NC} $SCRIPT_DIR"

# 1. Check Python 3
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[X] Error: python3 not found. Please install Python 3.${NC}"
    exit 1
fi

# 2. Check GTK3 and PyGObject dependencies
echo -e "${BLUE}[*] Checking Python and GTK dependencies...${NC}"
MISSING_DEPS=0

python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk, Gio, GLib" 2>/dev/null || MISSING_DEPS=1

if [ "$MISSING_DEPS" -eq 1 ]; then
    echo -e "${RED}[X] Error: GTK+ 3 or PyGObject dependencies missing!${NC}"
    echo -e "${YELLOW}To install required packages:${NC}"
    echo -e "  ${BOLD}Debian / Pardus / Ubuntu:${NC}"
    echo -e "    sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-glib-2.0 gir1.2-notify-0.7 gir1.2-pango-1.0 gvfs-fuse\n"
    echo -e "  ${BOLD}Arch Linux / Manjaro / CachyOS:${NC}"
    echo -e "    sudo pacman -S python-gobject gtk3 libnotify pango gvfs\n"
    exit 1
fi

# 3. Check version information
if [ ! -f "src/__version__" ] && [ -f "debian/changelog" ]; then
    VERSION=$(head -n 1 debian/changelog | sed -n 's/.*(\(.*\)).*/\1/p' || echo "0.1.0")
    echo "$VERSION" > "src/__version__" 2>/dev/null || true
fi

# 4. Prepare local translation (.mo) files if msgfmt is available
if command -v msgfmt &>/dev/null; then
    for po_file in po/*.po; do
        if [ -f "$po_file" ]; then
            lang=$(basename "$po_file" .po)
            target_dir="po/$lang/LC_MESSAGES"
            mo_file="$target_dir/pars-mycomputer.mo"
            if [ ! -f "$mo_file" ] || [ "$po_file" -nt "$mo_file" ]; then
                mkdir -p "$target_dir"
                msgfmt "$po_file" -o "$mo_file" 2>/dev/null || true
            fi
        fi
    done
fi

echo -e "${GREEN}[+] Dependencies verified. Launching application...${NC}\n"

# 5. Launch application
exec python3 "${SCRIPT_DIR}/src/Main.py" "$@"
