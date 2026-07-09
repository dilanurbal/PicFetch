"""
tests/mock_data.py

Testlerde (ve MOCK_MODE aktifken uygulamanin kendisinde) gercek Pixabay/Pexels
API'sine hic istek atmadan kullanilabilecek sahte gorsel veritabani ve
sahte arama surucusu.

Bu dosyadaki MOCK_DATABASE, daha once main.py icinde hardcoded olan
`mock_images_db` sozlugunun tasinmis halidir; main.py artik bu veriyi
buradan import ediyor.
"""

import os

# Kelime -> gorsel kayitlari. Her kayit gercek Unsplash URL'i, dogrulama
# durumu (is_verified) ve guven skoru (score) icerir.
MOCK_DATABASE = {
    "at": [
        {"url": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=800", "is_verified": True, "score": 0.94},
        {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": False, "score": 0.12},
        {"url": "https://images.unsplash.com/photo-1598974357801-cbca100e6543?w=800", "is_verified": True, "score": 0.88},
    ],
    "kedi": [
        {"url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800", "is_verified": True, "score": 0.96},
        {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": False, "score": 0.08},
        {"url": "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=800", "is_verified": True, "score": 0.91},
    ],
    "köpek": [
        {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": True, "score": 0.95},
        {"url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800", "is_verified": False, "score": 0.15},
        {"url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=800", "is_verified": True, "score": 0.89},
    ],
    "araba": [
        {"url": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800", "is_verified": True, "score": 0.97},
        {"url": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=800", "is_verified": False, "score": 0.11},
        {"url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800", "is_verified": True, "score": 0.92},
    ],
    "ev": [
        {"url": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800", "is_verified": True, "score": 0.93},
        {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": False, "score": 0.14},
        {"url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800", "is_verified": True, "score": 0.87},
    ],
    "ağaç": [
        {"url": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=800", "is_verified": True, "score": 0.98},
        {"url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800", "is_verified": False, "score": 0.05},
        {"url": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800", "is_verified": True, "score": 0.90},
    ],
    "çiçek": [
        {"url": "https://images.unsplash.com/photo-1526047932273-341f2a7631f9?w=800", "is_verified": True, "score": 0.97},
        {"url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800", "is_verified": False, "score": 0.09},
        {"url": "https://images.unsplash.com/photo-1561181286-d3fee7d55364?w=800", "is_verified": True, "score": 0.93},
    ],
    "kuş": [
        {"url": "https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=800", "is_verified": True, "score": 0.95},
        {"url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800", "is_verified": False, "score": 0.13},
        {"url": "https://images.unsplash.com/photo-1480069689960-5b3ff4b13390?w=800", "is_verified": True, "score": 0.87},
    ],
}


class MockSearchDriver:
    """
    core.search.ImageSearcher ile ayni genel arayuzu (search_images,
    download_image, is_valid_image) sunan, gercekte hicbir agi/HTTP
    istegi yapmayan sahte arama surucusu.

    Testlerde veya core.config.MOCK_MODE = True oldugunda gercek
    ImageSearcher'in yerine gecebilir.
    """

    def __init__(self, api_key: str = "mock_api_key"):
        self.api_key = api_key

    def search_images(self, query: str, per_page: int = 5) -> list:
        """MOCK_DATABASE'den, verilen kelimeye ait gorsel URL'lerini dondurur."""
        keyword = query.strip().lower()
        entries = MOCK_DATABASE.get(keyword)

        if entries is None:
            # Gercek ImageSearcher'in davranisina benzer sekilde,
            # bilinmeyen kelimeler icin bos liste donuyoruz.
            return []

        return [entry["url"] for entry in entries[:per_page]]

    def download_image(self, url: str, save_dir: str = "downloads") -> str:
        """Gercek bir indirme yapmadan, sahte bir gorsel dosyasi olusturur ve yolunu dondurur."""
        os.makedirs(save_dir, exist_ok=True)

        filename = url.split("/")[-1].split("?")[0] or "mock_image.jpg"
        filepath = os.path.join(save_dir, filename)

        with open(filepath, "wb") as f:
            f.write(b"MOCK_IMAGE_BYTES")

        return filepath

    def is_valid_image(self, filepath: str) -> bool:
        """Mock modda her uretilen dosya gecerli sayilir."""
        return os.path.exists(filepath)


def get_entries_for_keyword(keyword: str) -> list:
    """Yardimci fonksiyon: bir kelime icin MOCK_DATABASE kayitlarini dondurur (yoksa bos liste)."""
    return MOCK_DATABASE.get(keyword.strip().lower(), [])
