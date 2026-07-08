"""
test_search.py - core/search.py için testler.

ddgs gerçek internete bağlı olduğu için testlerde onu "mock"luyoruz
(sahte cevap veriyoruz). Böylece testler internet olsun olmasın,
ddgs o an çalışsın çalışmasın, hep aynı ve güvenilir sonucu verir.
"""

from unittest.mock import patch
from core.search import search_images

def test_search_images_returns_url_list():
    """
    ddgs sahte bir sonuç listesi döndürünce search_images bunu doğru bir url listesine çevirmeli
    """

    fake_results = [
        {"image": "https://ornek.com/kedi1.jpg"},
        {"image": "https://ornek.com/kedi2.jpg"}
    ]

    with patch("core.search.DDGS") as mock_ddgs:
        mock_ddgs.return_value.images.return_value = fake_results
        results = search_images("cat", limit=2)

    assert results == [
        "https://ornek.com/kedi1.jpg",
        "https://ornek.com/kedi2.jpg",
    ]

