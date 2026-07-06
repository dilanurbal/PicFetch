"""
search.py - Görsel Arama ve İndirme Modülü

Pixabay API'sini kullanarak görsel arar ve bulunan görselleri
geçici bir klasöre indirir.
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image

# Windows terminal emoji/unicode sorunlarını çözmek için UTF-8 yapılandırması
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# .env dosyasındaki değişkenleri yükle
load_dotenv()

class ImageSearcher:
    def __init__(self):
        # API Key'i .env dosyasından al
        self.api_key = os.getenv("PIXABAY_API_KEY")
        self.base_url = "https://pixabay.com/api/"
        
        if not self.api_key or self.api_key == "ornek_api_key_buraya":
            raise ValueError("HATA: .env dosyasında geçerli bir PIXABAY_API_KEY bulunamadı!")

    def is_valid_image(self, filepath: str) -> bool:
        """
        İndirilen dosyanın geçerli ve bozuk olmayan bir resim olup olmadığını kontrol eder.
        """
        try:
            with Image.open(filepath) as img:
                img.verify()  # Resmin gerçekten bir resim olup olmadığını doğrular
            return True
        except Exception:
            return False

    def search_images(self, query: str, per_page: int = 5) -> list:
        """
        Pixabay'de görsel arar.
        
        Args:
            query: Arama yapılacak İngilizce kelime (örn: "horse")
            per_page: Kaç tane görsel getirileceği
        
        Returns:
            Görsel URL'lerinin listesi
        """
        params = {
            "key": self.api_key,
            "q": query,
            "image_type": "photo",
            "per_page": per_page,
            "safesearch": "true"
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status() # Hata varsa durdur
            data = response.json()
            
            # Sadece büyük boyutlu görsel linklerini al
            image_urls = [hit["largeImageURL"] for hit in data.get("hits", [])]
            return image_urls
            
        except requests.exceptions.RequestException as e:
            print(f"API Hatası: {e}")
            return []

    def download_image(self, url: str, save_dir: str = "downloads") -> str:
        """
        Tek bir görseli indirir.
        
        Args:
            url: İndirilecek görselin linki
            save_dir: Kaydedileceği klasör
        
        Returns:
            İndirilen dosyanın tam yolu (başarılıysa), boş string (başarısızsa)
        """
        try:
            # Klasör yoksa oluştur
            Path(save_dir).mkdir(parents=True, exist_ok=True)
            
            # Görseli indir
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            # Dosya adı oluştur (URL'den son kısmı al)
            filename = url.split("/")[-1]
            filepath = os.path.join(save_dir, filename)
            
            # Dosyayı kaydet
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            # İndirilen dosyanın geçerli bir resim olup olmadığını kontrol et
            if not self.is_valid_image(filepath):
                print(f"⚠️ Bozuk dosya tespit edildi, siliniyor: {filepath}")
                os.remove(filepath) # Bozuk dosyayı sil
                return "" # Başarısız olduğunu belirtmek için boş string dön
            
            return filepath
            
        except Exception as e:
            print(f"İndirme Hatası ({url}): {e}")
            return ""


# Test etmek için
if __name__ == "__main__":
    print("🧪 Search Modülü Testi")
    print("=" * 40)
    
    # Arama yap
    searcher = ImageSearcher()
    urls = searcher.search_images("horse", per_page=3)
    
    print(f"Bulunan {len(urls)} görsel:")
    for url in urls:
        print(f"  - {url}")
    
    # İlk görseli indir
    if urls:
        print("\nİlk görsel indiriliyor...")
        filepath = searcher.download_image(urls[0])
        if filepath:
            print(f"✅ Başarıyla indirildi: {filepath}")
        else:
            print(" İndirme başarısız oldu.")