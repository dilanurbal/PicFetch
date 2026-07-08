"""
search.py - Görsel Arama Modülü

Verilen kelimeye göre görsel arar ve bulunan görsellerin
URL Listesini döndürür. İndirme modülü burada yok o pipeline'da.
"""

import sys
from ddgs import DDGS
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def search_images(query: str, limit: int = 10, max_attempts: int = 3) -> list[str]:
    for attempt in range(1, max_attempts + 1):
        try:
            result = DDGS().images(query, max_results=limit)
            urls =[r["image"] for r in result]
            return urls
        
        except Exception as e:
            print(f"Deneme {attempt}/{max_attempts} başarısız: {e}")

            if attempt < max_attempts:
                time.sleep(2)

    print(f"'{query}' için {max_attempts} denemede de sonuç alınamadı.")
    return []



if __name__ == "__main__":
    print("Search Modülü Testi")
    print(" ")

    found = search_images("dog", limit=10)
    print(f"Bulunan {len(found)} görsel: ")
    for url in found:
        print(f" - {url}")