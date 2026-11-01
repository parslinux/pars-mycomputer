# Pars Bilgisayarım - Mimari ve Tasarım (ARCHITECTURE.md)

Bu doküman, **Pars Bilgisayarım** (`pars-mycomputer`) uygulamasının mimari yapısını, temel bileşenlerini ve veri akışını açıklar.

---

## 🏛️ Genel Mimari

Uygulama, **Python 3** üzerinde **PyGObject** (GTK+ 3, GLib, Gio) kütüphaneleri kullanılarak geliştirilmiştir. Arayüz düzeni **Glade XML** (`ui/MainWindow.glade`) ve modern CSS kuralları (`css/style.css`) ile tanımlanmıştır.

```
+--------------------------------------------------------------------------+
|                               Main.py                                    |
|                       (Gtk.Application Başlatıcı)                         |
+--------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------+
|                            MainWindow.py                                 |
|               (Ana Pencere, Stack, Menü & Olay Yöneticisi)               |
+--------------------------------------------------------------------------+
       |                     |                       |               |
       v                     v                       v               v
+--------------+     +----------------+     +---------------+  +-----------+
| DiskManager  |     |FileBrowserView |     | UserSettings  |  |FstabWriter|
| (Disk/Bölüm) |     | (Dahili Tarayıcı)|   | (Ayar/Yapıland)| | (/etc/fstab)
+--------------+     +----------------+     +---------------+  +-----------+
```

---

## 🧩 Temel Modüller

### 1. `Main.py`
- Uygulamanın giriş noktasıdır (`Application` sınıfı).
- `application_id = "tr.org.pars.mycomputer"` kimliği ile GApplication döngüsünü başlatır ve `MainWindow`'u tetikler.

### 2. `MainWindow.py`
- Arayüzün merkezidir. Glade dosyasını yükler, sinyalleri bağlar.
- Stack yapısı (`stack_main`) ile farklı görünümler arasında geçiş yapar:
  - `home`: Ana diskler, bölümler ve çıkarılabilir aygıtlar görünümü.
  - `filebrowser`: Dahili dosya ve dizin tarayıcısı.
  - `settings`: Uygulama ayarları paneli.
  - `controlpanel`: Sistem denetim masası kısayolları.
- Sol taraftaki "Yerler" (Places) menüsünü (`Bilgisayar`, `Son Kullanılan`, `Çöp`, kullanıcı dizinleri) dinamik oluşturur.

### 3. `FileBrowserView.py`
- GTK `Box`, `TreeView` ve `ListStore` tabanlı dahili dosya yöneticisidir.
- **Dahili Özel Dizinler:**
  - `recent:///`: `Gtk.RecentManager` aracılığıyla son kullanılan dosyaları çeker.
  - `trash:///`: `Gio.File.new_for_uri("trash:///")` üzerinden çöp kutusu içeriklerini listeler.
- Dosya türlerine göre simgeleri dinamik çözümler (`_lookup_icon`), dosya boyutlarını ve tarihlerini biçimlendirir.

### 4. `DiskManager.py` & `Unmount.py`
- `Gio.VolumeMonitor` aracılığıyla sistemdeki bağlı ve ayrılmış diskleri, USB bellekleri ve optik sürücüleri izler.
- Disk bağlama (mount) ve güvenli ayırma (unmount) operasyonlarını yönetir.

### 5. `FstabWriter.py`
- Kalıcı disk bağlama yapılandırmaları için `/etc/fstab` dosyasını `pkexec` (Polkit) yetkisiyle güvenli şekilde günceller.

### 6. `UserSettings.py`
- `~/.config/pars-mycomputer/config.ini` dosyasında kullanıcı tercihlerini (koyu tema, son sunucular, otomatik yenileme vb.) saklar ve yönetir.

---

## 🔒 Güvenlik ve Yetkilendirme (Polkit)

Kök dizin ve fstab gibi sistem genelini etkileyen işlemler için Polkit kuralı (`tr.org.pars.pkexec.pars-mycomputer.policy`) devreye girer. Uygulama gereksiz yere baştan sona root olarak çalıştırılmaz, sadece yetki gerektiren kritik işlemlerde Polkit üzerinden parola istenir.
