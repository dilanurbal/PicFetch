"""
fetch.py - Görsel İndirme Modülü

Verilen bir URL'deki görseli sunucunun diskine indirir. Bu indirme,
YOLOE-26 doğrulaması içindir: model URL üzerinde değil, dosya üzerinde
çalıştığı için görselin önce diske inmesi gerekir. İndirme bir ara adımdır.

NOT: Bu, kullanıcının görsel indirmesi DEĞİLDİR. Kullanıcının doğrulanmış
görselleri kendi cihazına indirmesi ayrı bir iştir (main.py, ZIP indirme).
"""

import os
import uuid
import requests

# İndirilen görsellerin kaydedileceği klasör
DOWNLOAD_DIR = "downloads"


def download_image(url):
    """
    Verilen URL'deki görseli indirir ve diske kaydeder.

    Args:
        url: İndirilecek görselin adresi

    Returns:
        Kaydedilen dosyanın yolu, hata olursa None
    """
    # Klasör yoksa oluştur (her çağrıda kontrol etmek zararsız)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    try:
        # URL'ye git ve görseli indir (timeout: sonsuza kadar beklemesin)
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 404, 500 gibi hatalarda exception fırlatır

        # Her çağrıda benzersiz bir dosya adı üret (üst üste yazmayı önler)
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        # Görselin ham byte'larını diske yaz
        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath

    except Exception as e:
        # İndirme başarısız olursa çökme, None dön (pipeline atlar)
        print(f"İndirme başarısız ({url}): {e}")
        return None