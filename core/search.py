"""
search.py - Görsel Arama ve İndirme Modülü

Pixabay API'sini kullanarak görsel arar ve bulunan görselleri
geçici bir klasöre indirir. Rate limiting, cache ve retry logic içerir.
"""

import os
import sys
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import requests_cache
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Windows terminal emoji/unicode sorunlarını çözmek için UTF-8 yapılandırması
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# Cache ayarları - Aynı arama için tekrar API çağrısı yapma
requests_cache.install_cache(
    'pixabay_cache',  # Cache dosyası adı
    backend='sqlite',  # SQLite veritabanı kullan
    expire_after=3600  # 1 saat (3600 saniye) sonra cache temizlenir
)

class ImageSearcher:
    def __init__(self):
        # API Key'i .env dosyasından al
        self.api_key = os.getenv("PIXABAY_API_KEY")
        self.base_url = "https://pixabay.com/api/"
        self.last_request_time = 0  # Son istek zamanı
        self.min_request_interval = 1.0  # İstekler arası minimum süre (saniye)
        
        if not self.api_key or self.api_key == "ornek_api_key_buraya":
            raise ValueError("HATA: .env dosyasında geçerli bir PIXABAY_API_KEY bulunamadı!")

    def _rate_limit(self):
        """
        Rate limiting: İstekler arasında minimum bekleme süresi.
        Pixabay API'sinin hız limitine uymak için kullanılır.
        """
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            print(f"⏳ Rate limiting: {sleep_time:.2f} saniye bekleniyor...")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

    @retry(
        stop=stop_after_attempt(3),  # Maksimum 3 kez dene
        wait=wait_exponential(multiplier=1, min=2, max=10),  # 2, 4, 8 saniye bekle
        retry=retry_if_exception_type(requests.exceptions.RequestException)  # Sadece network hatalarında retry
    )
    def _make_api_request(self, params: dict) -> dict:
        """
        API'ye istek yapar. Hata olursa otomatik yeniden dener (retry logic).
        """
        self._rate_limit()  # Rate limiting uygula
        
        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()  # HTTP hatası varsa exception fırlat
        
        return response.json()

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
        Pixabay'de görsel arar. Cache kullanır - aynı sorgu için tekrar API çağrısı yapmaz.
        
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
            # Retry logic ile API'ye istek yap
            data = self._make_api_request(params)
            
            # Sadece büyük boyutlu görsel linklerini al
            image_urls = [hit["largeImageURL"] for hit in data.get("hits", [])]
            
            # Cache bilgisi göster
            if hasattr(requests_cache, 'get_cache'):
                cache_info = requests_cache.get_cache()
                if cache_info:
                    print(f"💾 Cache durumu: {len(cache_info.responses)} kayıtlı istek var")
            
            return image_urls
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Hatası (3 deneme sonrası): {e}")
            return []
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
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
    urls = searcher.search_images("cat", per_page=3)
    
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