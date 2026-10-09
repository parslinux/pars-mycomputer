# 1) 200MB boş dosya oluştur
fallocate -l 200M /tmp/test-disk.img

# 2) Loop device olarak bağla
sudo losetup -fP --show /tmp/test-disk.img
# → /dev/loop0 gibi bir şey döner

# 3) İçine bir bölüm tablosu + filesystem yaz (test için)
sudo mkfs.ext4 /dev/loop0

# 4) Uygulamayı aç, loop0 gözükmeli
python3 src/Main.py


Temizlik için:

sudo losetup -d /dev/loop0
rm /tmp/test-disk.img

Bunu otomatik yapan küçük bir test scripti yazayım mı? Şunları yapabilir:

Loop disk oluştur
İsteğe bağlı olarak ext4, ntfs, vfat formatla
Uygulamayı başlat
Çıkışta loop'u temizle
