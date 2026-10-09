# Maintainer: Pars Developers <dev@pars.org.tr>

pkgname=pars-mycomputer
pkgver=0.8.2
pkgrel=1
pkgdesc="Pars My Computer - UI for disk information and management"
arch=('any')
url="https://github.com/pars/pars-mycomputer"
license=('GPL3')
depends=('python' 'python-gobject' 'gtk3' 'libnotify' 'pango' 'gvfs')
makedepends=('python-setuptools' 'gettext')
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
  cd "$pkgname-$pkgver" 2>/dev/null || cd "$srcdir"
  python setup.py build
}

package() {
  cd "$pkgname-$pkgver" 2>/dev/null || cd "$srcdir"
  python setup.py install --root="$pkgdir" --optimize=1
}
