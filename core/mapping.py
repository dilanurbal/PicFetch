"""
mapping.py - Türkçe → İngilizce kelime eşleştirme modülü

Kullanıcı Türkçe bir kelime yazdığında (örn: "at"),
bunu İngilizce'ye çevirir ("horse").
Bu İngilizce kelime hem API aramasında hem YOLO modelinde kullanılacak.
"""
def turkish_lower(word: str) -> str:
    """
    Türkçe karakterleri düzgün küçük harfe çevirir.
    Python'ın normal .lower() fonksiyonu Türkçe 'İ' harfini
    yanlış çevirir, bu fonksiyon bunu düzeltir.
    """
    replacements = {
        "İ": "i",
        "I": "ı",
        "Ğ": "ğ",
        "Ü": "ü",
        "Ş": "ş",
        "Ö": "ö",
        "Ç": "ç",
    }
    for upper, lower in replacements.items():
        word = word.replace(upper, lower)
    return word.lower()

# Türkçe → İngilizce sözlük
# İstediğin kadar kelime ekleyebilirsin!
TURKISH_TO_ENGLISH = {
    # Hayvanlar
    "at": "horse",
    "köpek": "dog",
    "kedi": "cat",
    "kuş": "bird",
    "balık": "fish",
    "kurt": "wolf",
    "tilki": "fox",
    "ayı": "bear",
    "aslan": "lion",
    "kaplan": "tiger",
    "fil": "elephant",
    "zürafa": "giraffe",
    "maymun": "monkey",
    "tavşan": "rabbit",
    "fare": "mouse",
    "inek": "cow",
    "koyun": "sheep",
    "keçi": "goat",
    "domuz": "pig",
    "tavuk": "chicken",
    "ördek": "duck",
    "kartal": "eagle",
    "şahin": "falcon",
    "penguen": "penguin",
    "yunus": "dolphin",
    "köpekbalığı": "shark",
    "yılan": "snake",
    "kurbağa": "frog",
    "kaplumbağa": "turtle",
    "arı": "bee",
    "kelebek": "butterfly",
    
    # Nesneler
    "araba": "car",
    "bisiklet": "bicycle",
    "uçak": "airplane",
    "tren": "train",
    "gemi": "ship",
    "ev": "house",
    "ağaç": "tree",
    "çiçek": "flower",
    "kitap": "book",
    "bilgisayar": "computer",
    "telefon": "phone",
    "sandalye": "chair",
    "masa": "table",
    "saat": "clock",
    "anahtar": "key",
    "çanta": "bag",
    "şapka": "hat",
    "ayakkabı": "shoe",
    "gözlük": "glasses",
    
    # Yiyecekler
    "elma": "apple",
    "muz": "banana",
    "portakal": "orange",
    "domates": "tomato",
    "havuç": "carrot",
    "ekmek": "bread",
    "peynir": "cheese",
    "süt": "milk",
    "su": "water",
    "kahve": "coffee",
}


def translate_to_english(turkish_word: str) -> str:
    """
    Türkçe kelimeyi İngilizce'ye çevirir.
    
    Args:
        turkish_word: Türkçe kelime (örn: "at")
    
    Returns:
        İngilizce karşılığı (örn: "horse")
        Eğer kelime sözlükte yoksa, aynen döner.
    
    Örnek:
        >>> translate_to_english("at")
        'horse'
        >>> translate_to_english("bilmediğim")
        'bilmediğim'
    """
    # Küçük harfe çevir ve boşlukları temizle
    cleaned_word = turkish_lower(turkish_word).strip()
    
    # Sözlükte ara, yoksa aynen döndür
    return TURKISH_TO_ENGLISH.get(cleaned_word, cleaned_word)


def is_translatable(word: str) -> bool:
    """
    Kelimenin sözlükte olup olmadığını kontrol eder.
    
    Args:
        word: Kontrol edilecek kelime
    
    Returns:
        True eğer sözlükte varsa, False yoksa
    """
    return turkish_lower(word).strip() in TURKISH_TO_ENGLISH

# Bu dosyayı direkt çalıştırırsak test yapalım
if __name__ == "__main__":
    print("🧪 Mapping Modülü Testi")
    print("=" * 40)
    
    # Test 1: Bilinen kelime
    test_word = "at"
    result = translate_to_english(test_word)
    print(f"✅ '{test_word}' → '{result}'")
    
    # Test 2: Başka bir kelime
    test_word = "köpek"
    result = translate_to_english(test_word)
    print(f"✅ '{test_word}' → '{result}'")
    
    # Test 3: Büyük harfle yazılmış
    test_word = "KEDİ"
    result = translate_to_english(test_word)
    print(f"✅ '{test_word}' → '{result}'")
    
    # Test 4: Sözlükte olmayan kelime
    test_word = "bilmediğimkelime"
    result = translate_to_english(test_word)
    print(f"⚠️ '{test_word}' → '{result}' (sözlükte yok, aynen döndü)")
    
    # Test 5: is_translatable fonksiyonu
    print("\n🔍 Kelime sözlükte var mı?")
    print(f"  'at': {is_translatable('at')}")
    print(f"  'xyz': {is_translatable('xyz')}")
    
    print("\n✨ Tüm testler tamamlandı!")