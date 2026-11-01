# Sanal Test Alanı ve Çalıştırma Rehberi (`test_calistirmasi.md`)

Bu rehber, fiziksel bir USB bellek veya harici sabit disk takmaya gerek kalmadan, sanal bir disk (loop device) oluşturarak **Pars Bilgisayarım** uygulamasını tam fonksiyonel olarak test etmenizi sağlar.

---

## 🚀 1. Hızlı Başlatma (Tek Komutla Sanal Disk)

Test için 200MB boyutunda bir sanal disk oluşturup sisteme bağlamak için:

```bash
# 1) 200MB boş disk imajı oluştur
fallocate -l 200M /tmp/pars_test_disk.img

# 2) Loop aygıtı olarak sisteme bağla
sudo losetup -fP --show /tmp/pars_test_disk.img
# Bu komut çıktısı örn: /dev/loop0 döner.
```

### Diski Formatlama (Ext4, FAT32 veya NTFS):

**Ext4 (Linux Varsayılanı):**
```bash
sudo mkfs.ext4 -L "ParsTestDisk" /dev/loop0
```

*(İsteğe bağlı FAT32 formatı için: `sudo mkfs.vfat -F 32 -n "ParsUSB" /dev/loop0`)*

---

## 🖥️ 2. Pars Bilgisayarım Uygulamasını Çalıştırma

Proje ana dizinindeyken:

```bash
python3 src/Main.py
```

### ✅ Test Edilecek Senaryolar:

1. **Diski Görme:**
   - Sol/sağ listede `ParsTestDisk` görünmeli.
   - Durumu *"Disk kullanılabilir, bağlamak için tıklayın"* şeklinde olmalı.

2. **Bağlama (Mount):**
   - Diske tıklandığında disk bağlanmalı.
   - Boyut çubuğu (kullanılan/boş alan) dolmalı.
   - Ayarlarda *"Mount sonrası dosya yöneticisini otomatik aç"* açıksa belirlenen dosya yöneticisi (`nautilus`) açılmalı.

3. **Dosya Yöneticisi Ayarı:**
   - Sağ üstteki Ayarlar menüsünden dosya yöneticisi komutu (`nautilus`, `thunar`, `dolphin` vb.) değiştirilebilir.

4. **Ayırma (Unmount):**
   - Disk yanındaki çıkart / unmount butonuna basıldığında başarıyla unmount edilmeli.

---

## 🧹 3. Test Sonrası Temizlik

Test bittikten sonra sanal diski sistemden tamamen kaldırmak için:

```bash
# 1) Loop aygıtını serbest bırak
sudo losetup -d /dev/loop0

# 2) Geçici imaj dosyasını sil
rm -f /tmp/pars_test_disk.img
```

---

## ⚡ 4. Otomatik Test Scripti (İsteğe Bağlı)

İsterseniz aşağıdaki tek satırlık geçici test betiğini çalıştırabilirsiniz:

```bash
#!/usr/bin/env bash
set -e
IMG="/tmp/pars_test_disk.img"
echo ">> Sanal disk hazırlanıyor (200MB)..."
fallocate -l 200M "$IMG"
LOOP=$(sudo losetup -fP --show "$IMG")
echo ">> Bağlanan loop aygıtı: $LOOP"
sudo mkfs.ext4 -F -L "ParsTestDisk" "$LOOP"
echo ">> Pars MyComputer başlatılıyor..."
python3 src/Main.py
echo ">> Temizlik yapılıyor..."
sudo losetup -d "$LOOP"
rm -f "$IMG"
echo ">> Tamamlandı!"
```
