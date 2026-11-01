# Maintainer: Pars Linux <https://github.com/parslinux>
# Instagram: @parslinux

pkgname=pars-mycomputer
pkgver=0.8.2
pkgrel=1
pkgdesc="Pars My Computer - UI for disk information and management"
arch=('any')
url="https://github.com/parslinux"
license=('GPL3')
depends=('python' 'python-gobject' 'gtk3' 'libnotify' 'pango' 'gvfs')
makedepends=('gettext')
source=()
sha256sums=()

build() {
  cd "$startdir"
  for po in po/*.po; do
    [ -f "$po" ] || continue
    lang=$(basename "$po" .po)
    mkdir -p "po/$lang/LC_MESSAGES"
    msgfmt "$po" -o "po/$lang/LC_MESSAGES/pars-mycomputer.mo"
  done
}

package() {
  cd "$startdir"

  install -d "$pkgdir/usr/bin"
  install -m 755 pars-mycomputer "$pkgdir/usr/bin/"

  install -d "$pkgdir/usr/share/pars/pars-mycomputer"
  cp -r src ui css "$pkgdir/usr/share/pars/pars-mycomputer/"
  install -m 644 pars-mycomputer.svg "$pkgdir/usr/share/pars/pars-mycomputer/"

  install -d "$pkgdir/usr/share/pars/pars-mycomputer/autostart"
  install -m 755 autostart/pars-mycomputer-add-to-desktop "$pkgdir/usr/share/pars/pars-mycomputer/autostart/"

  install -d "$pkgdir/usr/share/applications"
  install -m 644 tr.org.pars.mycomputer.desktop "$pkgdir/usr/share/applications/"

  install -d "$pkgdir/usr/share/polkit-1/actions"
  install -m 644 tr.org.pars.pkexec.pars-mycomputer.policy "$pkgdir/usr/share/polkit-1/actions/"

  install -d "$pkgdir/etc/xdg/autostart"
  install -m 644 autostart/pars-mycomputer-add-to-desktop.desktop "$pkgdir/etc/xdg/autostart/"

  install -d "$pkgdir/usr/share/icons/hicolor/scalable/apps"
  install -m 644 pars-mycomputer*.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/"

  # Translations
  for po in po/*.po; do
    [ -f "$po" ] || continue
    lang=$(basename "$po" .po)
    install -d "$pkgdir/usr/share/locale/$lang/LC_MESSAGES"
    install -m 644 "po/$lang/LC_MESSAGES/pars-mycomputer.mo" "$pkgdir/usr/share/locale/$lang/LC_MESSAGES/"
  done
}
