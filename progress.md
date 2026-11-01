# 📊 Pars Bilgisayarım - Geliştirme İlerleme Takibi (progress.md)

Bu dosya, **Pars Bilgisayarım** (`pars-mycomputer`) projesindeki mevcut geliştirme durumunu, tamamlanan işleri ve gelecek planlarını takip eder.

---

## 🚀 Son Tamamlanan Görevler

| Görev / Özellik | Durum | Açıklama |
|---|:---:|---|
| **İngilizce Betikler (`run.sh`, `install.sh`, `uninstall.sh`)** | ✅ Tamamlandı | Tüm betik isimleri İngilizce yapıldı, otomatik sudo ve bağımlılık kontrolü eklendi. |
| **Evrensel Paketleme Betiği (`package.sh`)** | ✅ Tamamlandı | Arch (`.pkg.tar.zst`), Debian (`.deb`) ve Kaynak (`.tar.gz`) paketlerini tek komutla `dist/` klasörüne derler. |
| **Ekran Görüntüleri ve Görseller** | ✅ Tamamlandı | Eski Pardus PNG'leri kaldırıldı; canlı Pars temalı `pars-mycomputer-1.png` - `5.png` ve `pars-mycomputer.png` (256x256) üretildi. |
| **Dahili "Son Kullanılanlar" Desteği (`recent:///`)** | ✅ Tamamlandı | Harici dosya yöneticisi yerine `Gtk.RecentManager` entegrasyonu ile dahili tarayıcıda açılması sağlandı. |
| **Dahili "Çöp Kutusu" Desteği (`trash:///`)** | ✅ Tamamlandı | `Gio.File.new_for_uri("trash:///")` üzerinden silinen dosyaların dahili tarayıcıda listelenmesi sağlandı. |
| **Türkçe Dil Altyapısı Güçlendirmesi** | ✅ Tamamlandı | `locale.setlocale` aktif edildi, sistem ve yerel `po/` fallback mekanizması kuruldu; tüm menüler Türkçe yapıldı. |
| **İletişim & Çeviri Bilgileri Güncellemesi** | ✅ Tamamlandı | Çeviri (`po/`) ve Hakkında arayüzündeki eski şahsi e-postalar temizlendi; Pars Linux GitHub (`github.com/parslinux`) ve Instagram (`@parslinux`) eklendi. |
| **Dokümantasyon Yapılandırması (`docs/`)** | ✅ Tamamlandı | `INSTALL.md`, `fork.md`, `test_*.md` dosyaları `docs/` altına taşındı; `claude.md`, `.claudeignore` ve `progress.md` oluşturuldu. |

---

## 📈 Mevcut Durum Özeti

- **Sürüm:** 0.8.2
- **Aktif Dal:** main
- **Desteklenen Dağıtımlar:** Pars Linux, Arch Linux, CachyOS, Debian, Pardus, Ubuntu
- **Test Durumu:** Sanal disk (loop device) ve masaüstü X11 ortamında başarıyla test edildi.

---

## 🎯 Gelecek Planları (Roadmap)

- [ ] **GTK 4 & Libadwaita Geçiş Analizi:** Gelecek sürümler için modern GTK4 / Libadwaita port hazırlıkları.
- [ ] **Çöp Kutusu Geri Yükleme / Kalıcı Silme:** Dahili Çöp görünümünden sağ tıklama ile "Geri Yükle" ve "Tamamen Sil" aksiyonları.
- [ ] **Ağ Sürücüleri İyileştirmesi:** Samba / SFTP / NFS bağlantı sihirbazının arayüzünün daha da sadeleştirilmesi.
- [ ] **Bölümleme ve Biçimlendirme Aracı:** Gelişmiş disk formatlama seçenekleri (Btrfs, XFS, exFAT entegrasyonu).
