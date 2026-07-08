"""
search.py - Görsel Arama Modülü

Verilen kelimeye göre görsel arar ve bulunan görsellerin
URL Listesini döndürür. İndirme modülü burada yok o pipeline'da.
"""

import sys
from ddgs import DDGS

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def search_images(query: str, limit: int = 10) -> list[str]:
    results = DDGS().images(query, max_results=limit)

    urls = [r["image"] for r in results]

    return urls


if __name__ == "__main__":
    print("Search Modülü Testi")
    print(" ")

    found = search_images("dog", limit=50)
    print(f"Bulunan {len(found)} görsel: ")
    for url in found:
        print(f" - {url}")