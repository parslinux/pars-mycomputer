#!/usr/bin/env bash
# ==============================================================================
# Pars My Computer - System Uninstallation Script
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
    echo -e "${YELLOW}[!] Root privileges required for uninstallation.${NC}"
    echo -e "${BLUE}[*] Requesting sudo permissions...${NC}"
    exec sudo bash "$0" "$@"
fi

echo -e "${RED}${BOLD}====================================================${NC}"
echo -e "${CYAN}${BOLD}       Pars My Computer - Uninstaller               ${NC}"
echo -e "${RED}${BOLD}====================================================${NC}"

# Confirmation prompt unless -y, --yes, or -f is passed
AUTO_CONFIRM=0
for arg in "$@"; do
    if [ "$arg" == "-y" ] || [ "$arg" == "--yes" ] || [ "$arg" == "-f" ]; then
        AUTO_CONFIRM=1
        break
    fi
done

if [ "$AUTO_CONFIRM" -eq 0 ]; then
    read -rp "Are you sure you want to completely uninstall Pars My Computer? [Y/n]: " response
    case "$response" in
        [yY][eE][sS]|[yY]|"")
            ;;
        *)
            echo -e "${YELLOW}[!] Uninstallation cancelled.${NC}"
            exit 0
            ;;
    esac
fi

echo -e "\n${BLUE}[*] Removing installed application files...${NC}"

# Target files and directories to remove
REMOVE_TARGETS=(
    "/usr/bin/pars-mycomputer"
    "/usr/share/pars/pars-mycomputer"
    "/usr/share/applications/tr.org.pars.mycomputer.desktop"
    "/usr/share/polkit-1/actions/tr.org.pars.pkexec.pars-mycomputer.policy"
    "/etc/xdg/autostart/pars-mycomputer-add-to-desktop.desktop"
    "/usr/share/icons/hicolor/scalable/apps/pars-mycomputer.svg"
    "/usr/share/icons/hicolor/scalable/apps/pars-mycomputer-emblem-pars-symbolic.svg"
)

for target in "${REMOVE_TARGETS[@]}"; do
    if [ -e "$target" ]; then
        echo -e "  - Removing: $target"
        rm -rf "$target"
    fi
done

# Remove translation files (.mo)
for mo in /usr/share/locale/*/LC_MESSAGES/pars-mycomputer.mo; do
    if [ -f "$mo" ]; then
        echo -e "  - Removing locale file: $mo"
        rm -f "$mo"
    fi
done

# Clean Python package residues
find /usr/lib /usr/local/lib -maxdepth 4 -type d -name "pars_mycomputer*" 2>/dev/null | while read -r pydir; do
    echo -e "  - Removing Python package residue: $pydir"
    rm -rf "$pydir"
done

# Update system caches
echo -e "\n${BLUE}[*] Updating desktop and icon caches...${NC}"
if command -v gtk-update-icon-cache &>/dev/null; then
    gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor 2>/dev/null || true
fi
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database -q /usr/share/applications 2>/dev/null || true
fi

echo -e "\n${GREEN}${BOLD}====================================================${NC}"
echo -e "${GREEN}${BOLD}   [✓] Pars My Computer Successfully Uninstalled!   ${NC}"
echo -e "${GREEN}${BOLD}====================================================${NC}\n"
