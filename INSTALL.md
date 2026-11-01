# Pars Bilgisayarım - Kurulum Rehberi (INSTALL.md)

Bu doküman, **Pars Bilgisayarım** (`pars-mycomputer`) uygulamasını kaynak koddan çalıştırma, Debian/Pardus/Ubuntu ve Arch Linux sistemlerine kurma adımlarını içerir.

---

## 1. Bağımlılıklar (Dependencies)

Uygulama **Python 3** ve **GTK+ 3** tabanlıdır.

### Debian / Ubuntu / Pardus:
```bash
sudo apt update
sudo apt install -y \
    python3 \
    python3-gi \
    python3-setuptools \
    gir1.2-glib-2.0 \
    gir1.2-gtk-3.0 \
    gir1.2-notify-0.7 \
    gir1.2-pango-1.0 \
    gvfs-fuse \
    gettext
```

### Arch Linux / Manjaro / EndeavourOS:
```bash
sudo pacman -S --needed \
    python \
    python-gobject \
    python-setuptools \
    gtk3 \
    libnotify \
    pango \
    gvfs \
    gettext
```

---

## 2. Kaynak Koddan Çalıştırma (Run from Source)

Uygulamayı sisteme kurmadan doğrudan yerel kaynak kod üzerinden çalıştırmak için:

```bash
cd /path/to/pars-mycomputer
./run.sh
```
*(veya doğrudan: `python3 src/Main.py`)*

---

## 3. Sistem Geneline Kurulum (Setup.py veya install.sh ile Yükleme)

Uygulamayı tüm Linux dağıtımlarında doğrudan sistem dizinlerine yüklemek için:

```bash
sudo ./install.sh
```
*(veya klasik yöntem: `sudo python3 setup.py install`)*

Kurulumdan sonra terminalden çalıştırmak için:
```bash
pars-mycomputer
```

---

## 4. Paketleme Betiği ile Otomatik Paket Oluşturma (`package.sh`)

Tüm Linux dağıtımları için paketleri tek komutla `dist/` dizinine derlemek için:

```bash
# Tüm paketleri derler (Arch .pkg.tar.zst, Debian .deb, Source .tar.gz)
./package.sh all

# Veya sadece istediğiniz format:
./package.sh arch    # Arch Linux (.pkg.tar.zst)
./package.sh deb     # Debian / Ubuntu / Pardus (.deb)
./package.sh tar     # Kaynak kod arşiv paketi (.tar.gz)
```

---

## 5. Manuel Paket Oluşturma Yöntemleri

### Arch Linux (PKGBUILD / makepkg):
```bash
makepkg -si
```

### Debian / Pardus / Ubuntu (.deb):
```bash
sudo apt install -y devscripts git-buildpackage build-essential debhelper
gbp buildpackage --git-export-dir=/tmp/build/pars-mycomputer -us -uc
sudo dpkg -i ../pars-mycomputer_*.deb
```

---

## 6. Uygulamayı Kaldırma (Uninstall)
 
### Betik ile Otomatik Kaldırma (Tüm Dağıtımlar):
```bash
sudo ./uninstall.sh
```

### Arch Linux (pacman ile kurulduysa):
```bash
sudo pacman -R pars-mycomputer
```

### Debian / Pardus / Ubuntu (apt ile kurulduysa):
```bash
sudo apt remove pars-mycomputer
```

### Manuel Kaldırma:
```bash
sudo rm -rf /usr/share/pars/pars-mycomputer
sudo rm -f /usr/bin/pars-mycomputer
sudo rm -f /usr/share/applications/tr.org.pars.mycomputer.desktop
sudo rm -f /usr/share/polkit-1/actions/tr.org.pars.pkexec.pars-mycomputer.policy
sudo rm -f /etc/xdg/autostart/pars-mycomputer-add-to-desktop.desktop
sudo rm -f /usr/share/icons/hicolor/scalable/apps/pars-mycomputer*.svg
sudo rm -f /usr/share/locale/*/LC_MESSAGES/pars-mycomputer.mo
```
