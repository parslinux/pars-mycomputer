# Pars Bilgisayarım - Geliştirici Kılavuzu (DEVELOPMENT.md)

Bu kılavuz, **Pars Bilgisayarım** (`pars-mycomputer`) projesine katkıda bulunmak isteyen geliştiriciler için iş akışlarını, betikleri ve test süreçlerini anlatır.

---

## 🛠️ Geliştirme Ortamı Kurulumu

Gerekli paketleri sisteminize kurun:

### Debian / Pardus / Ubuntu:
```bash
sudo apt update
sudo apt install -y python3 python3-gi gir1.2-gtk-3.0 gir1.2-glib-2.0 gir1.2-notify-0.7 gir1.2-pango-1.0 gvfs-fuse gettext
```

### Arch Linux / Manjaro / CachyOS:
```bash
sudo pacman -S --needed python python-gobject gtk3 libnotify pango gvfs gettext
```

---

## 🚀 Çalıştırma ve Test

Uygulamayı derlemeye veya kurmaya gerek kalmadan doğrudan kaynak kod üzerinden çalıştırmak için:

```bash
./run.sh
```

*(Bu betik Python bağımlılıklarını denetler, `src/__version__` dosyasını hazırlar, yerel çeviri `.mo` dosyalarını derler ve uygulamayı başlatır.)*

### Sanal Disk ile Test:
Fiziksel disk takmadan test senaryolarını çalıştırmak için `docs/test_calistirmasi.md` rehberine göz atabilirsiniz.

---

## 🌐 Çevirileri Güncelleme (i18n / gettext)

Yeni bir arayüz metni eklediğinizde veya mevcut metinleri güncellediğinizde:

1. `po/files` dosyasının taranacak kaynak dosyaları içerdiğinden emin olun (`ui/MainWindow.glade`, `src/MainWindow.py`, `src/UserSettings.py`, `src/FileBrowserView.py`).
2. Çeviri şablonunu ve `.po` dosyalarını güncelleyin:
   ```bash
   ./update-translations.sh
   ```
3. `po/tr.po` dosyasındaki yeni `msgid` girdilerini `msgstr` olarak çevirin.
4. `.mo` ikili dosyalarını derleyin:
   ```bash
   mkdir -p po/tr/LC_MESSAGES
   msgfmt po/tr.po -o po/tr/LC_MESSAGES/pars-mycomputer.mo
   ```

---

## 📦 Paketleme

Projeyi dağıtılabilir paketler haline getirmek için:

```bash
./package.sh all
```

Üretilen paketler:
- `dist/pars-mycomputer-*.pkg.tar.zst` (Arch / Pacman)
- `dist/pars-mycomputer_*_all.deb` (Debian / Pardus / APT)
- `dist/pars-mycomputer-*.tar.gz` (Universal Kaynak Kod Arşivi)
