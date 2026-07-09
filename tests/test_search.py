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

    # DDGS'yi kullanıldığı yerde (core.search içinde) patch'liyoruz, tanımlandığı
    # yerde (ddgs paketinde) değil; çünkü search.py kendi içindeki adı kullanıyor.
    with patch("core.search.DDGS") as mock_ddgs:
        # Zincir: DDGS() -> nesne (1. return_value), .images() -> sonuç (2. return_value)
        mock_ddgs.return_value.images.return_value = fake_results
        results = search_images("cat", limit=2)

    assert results == [
        "https://ornek.com/kedi1.jpg",
        "https://ornek.com/kedi2.jpg",
    ]

def test_search_images_empty_result():
    """
    ddgs boş liste döndürünce (hiç sonuç yok), search_images de
    çökmeden boş liste döndürmeli.
    """
    with patch("core.search.DDGS") as mock_ddgs:
        mock_ddgs.return_value.images.return_value = []
        results = search_images("asdfqwerty", limit=5)

    assert results == []


def test_search_images_all_attempts_fail():
    """
    ddgs her denemede hata fırlatırsa (örn. internet kesintisi),
    search_images çökmeden retry yapmalı ve sonunda boş liste döndürmeli.
    """
    with patch("core.search.DDGS") as mock_ddgs, \
         patch("core.search.time.sleep"):

        # side_effect (return_value değil): mock çağrılınca değer döndürmek yerine hata fırlatır
        mock_ddgs.return_value.images.side_effect = Exception("baglanti hatasi")

        results = search_images("cat", limit=5, max_attempts=3)

    assert results == []

    # Retry'ın kalbi: images() 3 kez çağrıldıysa kod gerçekten 3 kez denemiş demektir
    assert mock_ddgs.return_value.images.call_count == 3