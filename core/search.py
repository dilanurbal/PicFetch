"""
search.py - Görsel Arama Modülü

DuckDuckGo Images API'sini kullanarak görsel arar ve bulunan görsellerin
URL Listesini döndürür. Retry logic ile hata toleransı sağlar.
"""

import sys
import time
from ddgs import DDGS

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def search_images(query: str, limit: int = 10, max_attempts: int = 3) -> list[str]:
    """
    DuckDuckGo'da görsel arar.
    
    Args:
        query: Arama yapılacak kelime
        limit: Kaç tane görsel getirileceği
        max_attempts: Başarısız olursa kaç kez tekrar dene
    
    Returns:
        Görsel URL'lerinin listesi
    """
    for attempt in range(1, max_attempts + 1):
        try:
            result = DDGS().images(query, max_results=limit)
            urls = [r["image"] for r in result]
            return urls
        
        except Exception as e:
            print(f"Deneme {attempt}/{max_attempts} başarısız: {e}")
            
            if attempt < max_attempts:
                time.sleep(2)
    
    print(f"'{query}' için {max_attempts} denemede de sonuç alınamadı.")
    return []


if __name__ == "__main__":
    print("🧪 Search Modülü Testi")
    print("=" * 40)
    
    found = search_images("dog", limit=10)
    print(f"Bulunan {len(found)} görsel:")
    for url in found:
        print(f"  - {url}")