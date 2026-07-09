"""
mock_data.py - Geliştirme Aşaması İçin Sahte Veriler

Gerçek API limitlerini harcamamak için statik JSON verileri.
Hem Türkçe hem İngilizce anahtar kelimeleri destekler.
"""

from typing import List, Dict

# At / Horse görselleri
HORSE_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2020/03/12/15/33/horse-4925003_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "horse, animal, nature",
        "is_verified": True,
        "score": 0.94
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2018/06/19/18/20/horses-3484123_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "horses, field, grass",
        "is_verified": False,
        "score": 0.12
    },
    {
        "id": 3,
        "url": "https://cdn.pixabay.com/photo/2019/10/15/10/30/horse-4551725_1280.jpg",
        "width": 1280,
        "height": 1920,
        "tags": "horse, portrait, animal",
        "is_verified": True,
        "score": 0.88
    },
]

# Köpek / Dog görselleri
DOG_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2019/12/20/15/47/dog-4708111_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "dog, animal, pet",
        "is_verified": True,
        "score": 0.95
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2020/01/02/07/16/dog-4735547_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "dog, puppy, cute",
        "is_verified": False,
        "score": 0.15
    },
]

# Kedi / Cat görselleri
CAT_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083408_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "cat, animal, pet",
        "is_verified": True,
        "score": 0.96
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2014/12/21/23/37/cat-575924_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "cat, kitten, cute",
        "is_verified": False,
        "score": 0.08
    },
]

# Araba / Car görselleri
CAR_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2012/11/02/13/02/car-63930_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "car, vehicle, auto",
        "is_verified": True,
        "score": 0.97
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "tree",
        "is_verified": False,
        "score": 0.11
    },
    {
        "id": 3,
        "url": "https://cdn.pixabay.com/photo/2016/11/22/23/44/porsche-1851246_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "car, porsche",
        "is_verified": True,
        "score": 0.92
    }
]

# Ev / House görselleri
HOUSE_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2016/11/18/17/46/house-1836070_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "house, building, home",
        "is_verified": True,
        "score": 0.93
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2016/11/14/17/39/dog-1824166_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "dog",
        "is_verified": False,
        "score": 0.14
    },
    {
        "id": 3,
        "url": "https://cdn.pixabay.com/photo/2014/07/10/17/18/large-home-389271_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "house, luxury",
        "is_verified": True,
        "score": 0.87
    }
]

# Ağaç / Tree görselleri
TREE_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "tree, green, nature",
        "is_verified": True,
        "score": 0.98
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "cat",
        "is_verified": False,
        "score": 0.05
    },
    {
        "id": 3,
        "url": "https://cdn.pixabay.com/photo/2015/06/08/15/02/forest-801757_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "forest, trees",
        "is_verified": True,
        "score": 0.90
    }
]

# Çiçek / Flower görselleri
FLOWER_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2014/02/27/16/10/flowers-276014_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "flowers, nature",
        "is_verified": True,
        "score": 0.97
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "cat",
        "is_verified": False,
        "score": 0.09
    },
    {
        "id": 3,
        "url": "https://cdn.pixabay.com/photo/2015/04/19/08/32/rose-729509_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "rose, flower",
        "is_verified": True,
        "score": 0.93
    }
]

# Kuş / Bird görselleri
BIRD_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2015/11/16/16/28/bird-1045954_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "bird, nature, animal",
        "is_verified": True,
        "score": 0.95
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2016/11/14/17/39/dog-1824166_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "dog",
        "is_verified": False,
        "score": 0.13
    },
    {
        "id": 3,
        "url": "https://cdn.pixabay.com/photo/2017/05/08/13/15/bird-2295431_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "bird, flying",
        "is_verified": True,
        "score": 0.87
    }
]

# Balık / Fish görselleri
FISH_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2016/11/04/13/05/fish-1797762_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "fish, aquarium, under water",
        "is_verified": True,
        "score": 0.96
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "cat, pet",
        "is_verified": False,
        "score": 0.05
    }
]

# Kitap / Book görselleri
BOOK_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2016/09/08/22/43/books-1655783_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "books, library, study",
        "is_verified": True,
        "score": 0.98
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2016/11/14/17/39/dog-1824166_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "dog",
        "is_verified": False,
        "score": 0.02
    }
]

# Bilgisayar / Computer görselleri
COMPUTER_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2014/09/24/14/29/macbook-459196_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "computer, laptop, workspace",
        "is_verified": True,
        "score": 0.97
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2016/11/18/17/46/house-1836070_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "house",
        "is_verified": False,
        "score": 0.12
    }
]

# Telefon / Phone görselleri
PHONE_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2016/11/29/05/07/smart-phone-1867451_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "phone, smart phone, mobile",
        "is_verified": True,
        "score": 0.95
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2014/12/21/23/37/cat-575924_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "cat",
        "is_verified": False,
        "score": 0.10
    }
]

# Elma / Apple görselleri
APPLE_IMAGES = [
    {
        "id": 1,
        "url": "https://cdn.pixabay.com/photo/2016/08/12/10/00/apple-1588078_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "apple, red apple, fruit",
        "is_verified": True,
        "score": 0.96
    },
    {
        "id": 2,
        "url": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg",
        "width": 1280,
        "height": 853,
        "tags": "tree",
        "is_verified": False,
        "score": 0.15
    }
]

# Sahte görsel veri tabanı (Hem Türkçe hem İngilizce kelimeleri destekler)
MOCK_IMAGE_DATA = {
    # Türkçe Anahtarlar
    "at": HORSE_IMAGES,
    "kedi": CAT_IMAGES,
    "köpek": DOG_IMAGES,
    "araba": CAR_IMAGES,
    "ev": HOUSE_IMAGES,
    "ağaç": TREE_IMAGES,
    "çiçek": FLOWER_IMAGES,
    "kuş": BIRD_IMAGES,
    "balık": FISH_IMAGES,
    "kitap": BOOK_IMAGES,
    "bilgisayar": COMPUTER_IMAGES,
    "telefon": PHONE_IMAGES,
    "elma": APPLE_IMAGES,
    
    # İngilizce Anahtarlar
    "horse": HORSE_IMAGES,
    "cat": CAT_IMAGES,
    "dog": DOG_IMAGES,
    "car": CAR_IMAGES,
    "house": HOUSE_IMAGES,
    "tree": TREE_IMAGES,
    "flower": FLOWER_IMAGES,
    "bird": BIRD_IMAGES,
    "fish": FISH_IMAGES,
    "book": BOOK_IMAGES,
    "computer": COMPUTER_IMAGES,
    "phone": PHONE_IMAGES,
    "apple": APPLE_IMAGES,
}


def get_mock_images(query: str, per_page: int = 5) -> List[Dict]:
    """
    Sorguya uygun statik sahte görselleri döndürür.
    Bulunamazsa dinamik/sahte görseller üretir.
    
    Args:
        query: Arama sorgusu
        per_page: Maksimum sonuç sayısı
        
    Returns:
        Sahte görsel nesneleri listesi (url, is_verified, score içeren)
    """
    query_lower = query.lower().strip()
    
    if query_lower in MOCK_IMAGE_DATA:
        images = MOCK_IMAGE_DATA[query_lower]
    else:
        # Kelime uzunluğuna göre hafifçe değişen dinamik skorlar ve varsayılan manzara görselleri
        val = len(query) % 10
        score1 = round(0.90 + (val / 150), 2)
        score2 = round(0.10 + (val / 150), 2)
        score3 = round(0.80 + (val / 150), 2)
        images = [
            {
                "id": 1,
                "url": "https://cdn.pixabay.com/photo/2016/08/11/23/48/mountains-1587287_1280.jpg",
                "width": 1280,
                "height": 853,
                "tags": "mountains, nature",
                "is_verified": True,
                "score": score1
            },
            {
                "id": 2,
                "url": "https://cdn.pixabay.com/photo/2016/11/14/17/39/dog-1824166_1280.jpg",
                "width": 1280,
                "height": 853,
                "tags": "dog, puppy",
                "is_verified": False,
                "score": score2
            },
            {
                "id": 3,
                "url": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg",
                "width": 1280,
                "height": 853,
                "tags": "tree, green",
                "is_verified": True,
                "score": score3
            }
        ]
        
    return images[:per_page]