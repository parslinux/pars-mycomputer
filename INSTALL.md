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
python3 src/Main.py
```

---

## 3. Sistem Geneline Kurulum (Setup.py ile Yükleme)

Uygulamayı tüm Linux dağıtımlarında doğrudan sistem dizinlerine yüklemek için:

```bash
sudo python3 setup.py install
```

Kurulumdan sonra terminalden çalıştırmak için:
```bash
pars-mycomputer
```

---

## 4. Arch Linux Paketi Oluşturma (PKGBUILD / makepkg)

Arch Linux üzerinde `.pkg.tar.zst` paketi derleyip yüklemek için:

1. Proje dizinindeki `PKGBUILD` dosyasını kullanarak paketi derleyin:
   ```bash
   makepkg -si
   ```

---

## 5. `.deb` Paketi Oluşturma (Debian/Pardus/Ubuntu Packaging)

1. Derleme araçlarını yükleyin:
   ```bash
   sudo apt install -y devscripts git-buildpackage build-essential debhelper
   ```

2. `.deb` paketini derleyin:
   ```bash
   gbp buildpackage --git-export-dir=/tmp/build/pars-mycomputer -us -uc
   ```

3. Paket yükleme:
   ```bash
   sudo dpkg -i ../pars-mycomputer_*.deb
   sudo apt install -f
   ```

---

## 6. Uygulamayı Kaldırma (Uninstall)

### Arch Linux (pacman):
```bash
sudo pacman -R pars-mycomputer
```

### Debian / Pardus / Ubuntu (apt):
```bash
sudo apt remove pars-mycomputer
```

### `setup.py` ile Yapılan Kurulumu Kaldırma:
```bash
sudo rm -rf /usr/share/pars/pars-mycomputer
sudo rm -f /usr/bin/pars-mycomputer
sudo rm -f /usr/share/applications/tr.org.pars.mycomputer.desktop
sudo rm -f /usr/share/polkit-1/actions/tr.org.pars.pkexec.pars-mycomputer.policy
sudo rm -f /etc/xdg/autostart/pars-mycomputer-add-to-desktop.desktop
sudo rm -f /usr/share/icons/hicolor/scalable/apps/pars-mycomputer*.svg
```
