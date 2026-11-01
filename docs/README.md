# Pars Bilgisayarım - Dokümantasyon İndeksi (docs/)

Bu dizin, **Pars Bilgisayarım** (`pars-mycomputer`) projesinin tüm teknik, kurulum, test ve geliştirme belgelerini barındırır.

---

## 📚 Doküman Listesi

1. **[INSTALL.md](INSTALL.md):** 
   - Ayrıntılı kurulum kılavuzu.
   - Bağımlılıklar, kaynak koddan çalıştırma, sistem geneline kurma, `.deb` ve Arch `.pkg.tar.zst` paketleme adımları.

2. **[ARCHITECTURE.md](ARCHITECTURE.md):**
   - Uygulama mimarisi, modüllerin görevleri (`MainWindow`, `FileBrowserView`, `DiskManager`, `FstabWriter`, `UserSettings`).
   - Sinyal akışı ve GIO/Polkit entegrasyonu.

3. **[DEVELOPMENT.md](DEVELOPMENT.md):**
   - Geliştirici kılavuzu.
   - Betiklerin kullanımı (`run.sh`, `install.sh`, `uninstall.sh`, `package.sh`).
   - Çeviri güncelleme ve derleme süreci.

4. **[test_calistirmasi.md](test_calistirmasi.md):**
   - Sanal test alanı hazırlama rehberi.
   - Fiziksel diske gerek kalmadan loop device üzerinden disk bağlama, biçimlendirme ve test adımları.

5. **[test_sanal.md](test_sanal.md):**
   - Hızlı sanal disk test kılavuzu.

6. **[fork.md](fork.md):**
   - Projenin çatallanma (fork) bilgileri, Pars Linux ekosistemi uyarlamaları, lisans ve telif hakları bildirimi.
