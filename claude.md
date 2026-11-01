# Claude AI Assistant Guide - Pars My Computer (`pars-mycomputer`)

Bu doküman, **Pars Bilgisayarım** projesinde Claude AI ve geliştiriciler için temel rehber, mimari özet, komutlar ve kuralları içerir.

---

## 📌 Proje Özeti

- **Uygulama Adı:** Pars Bilgisayarım (`pars-mycomputer`)
- **Ekosistem:** Pars Linux
- **Teknoloji:** Python 3, GTK+ 3 (PyGObject), Glade, Gio/Glib
- **Amaç:** Bilgisayardaki dahili ve harici diskleri, USB bellekleri, ağ paylaşımlarını yönetmek, sistem bilgilerini sunmak ve dahili dosya tarayıcısı ile dizin/dosya içeriklerini görüntülemek.

---

## 🛠️ Temel Betikler ve Komutlar

| Betik | Görevi | Çalıştırma |
|---|---|---|
| `run.sh` | Kaynak koddan uygulamayı başlatır (bağımlılıkları ve çevirileri otomatik denetler) | `./run.sh` |
| `install.sh` | Uygulamayı sistem geneline kurar (`/usr/bin`, `/usr/share/pars/`, ikonlar, polkit, vb.) | `sudo ./install.sh` |
| `uninstall.sh` | Uygulamayı sistemden temiz şekilde kaldırır | `sudo ./uninstall.sh` |
| `package.sh` | Arch Linux (`.pkg.tar.zst`), Debian (`.deb`) ve Kaynak (`.tar.gz`) paketlerini `dist/` dizinine derler | `./package.sh [all\|arch\|deb\|tar]` |
| `update-translations.sh` | Çeviri şablonunu (`po/pars-mycomputer.pot`) ve dil dosyalarını (`po/*.po`) günceller | `./update-translations.sh` |

---

## 🏛️ Mimari ve Dizin Yapısı

```
parslinux-mycomputer/
├── autostart/             # Otomatik masaüstü kısayolu oluşturma betiği ve .desktop
├── css/                   # GTK CSS stil dosyaları (style.css)
├── debian/                # Debian paketleme kuralları, changelog ve control dosyaları
├── dist/                  # package.sh tarafından üretilen paketler (gitignore'lu)
├── docs/                  # Kapsamlı proje dokümantasyonu
├── po/                    # Çeviri dosyaları (.po, .pot, .mo)
├── screenshots/           # Uygulama ekran görüntüleri (pars-mycomputer-*.png)
├── src/                   # Python kaynak kodları
│   ├── Main.py            # Gtk.Application giriş noktası
│   ├── MainWindow.py      # Ana pencere ve arayüz mantığı
│   ├── FileBrowserView.py # Dahili dosya ve dizin tarayıcısı (Trash & Recent dahil)
│   ├── DiskManager.py     # Disk ve bölümleme algılama/yönetim
│   ├── FstabWriter.py     # /etc/fstab yapılandırma yazıcısı
│   ├── Unmount.py         # Güvenli disk ayırma işlemleri
│   ├── UserSettings.py    # Kullanıcı ayarları (ini tabanlı)
│   └── __version__        # Sürüm numarası
├── ui/                    # Glade arayüz dosyaları (MainWindow.glade)
├── PKGBUILD               # Arch Linux paket tanımlayıcısı
├── setup.py               # Python setuptools yapılandırması
├── .claudeignore          # Claude yapay zeka hariç tutma kuralları
├── progress.md            # Geliştirme ilerleme ve durum takip tablosu
└── README.md              # Proje tanıtım ve vitrin sayfası
```

---

## 💡 Geliştirici & Claude İlkeleri

1. **Dil Uyumu:** Arayüz metinleri varsayılan olarak Türkçe olmalı ve `gettext` şablonlarına uygun şekilde yazılmalıdır.
2. **Dahili Dosya Tarayıcısı:** `recent:///` (Son Kullanılanlar) ve `trash:///` (Çöp) özel dizinleri `FileBrowserView` bileşeni içinde yerel olarak açılmalıdır; harici uygulamaya yönlendirilmemelidir.
3. **Paketleme Güvenliği:** `package.sh` betiği hem Arch hem Debian paketlerini harici karmaşık bağımlılıklara ihtiyaç duymadan temiz bir şekilde `dist/` dizininde üretmelidir.
4. **Dokümantasyon:** Yeni belgeler `docs/` klasörü altında yapılandırılmalı ve `progress.md` güncel tutulmalıdır.
