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


def translate_query(word: str, translate: bool = False, target_lang: str = "tr") -> str:
    """
    Sadece translate=True olduğunda kelimeyi İngilizce'ye çevirir.
    Tek Sorumluluk Prensibi (SRP): Çeviri kararını ve sözlük aramasını yönetir.
    
    Args:
        word: Arama yapılacak kelime
        translate: Çeviri yapılıp yapılmayacağı
        target_lang: Kaynak/hedef dil
        
    Returns:
        İngilizce karşılığı (çeviri aktifse ve bulunursa), aksi halde kelimenin kendisi.
    """
    if translate:
        return translate_to_english(word)
    return word


# Bu dosyayı direkt çalıştırırsak test yapalım
if __name__ == "__main__":
    print("🧪 Mapping Modülü Testi")
    print("=" * 40)
    
    # Test: translate_query
    print("🔄 translate_query (translate=True) testi:")
    print(f"  'at' -> {translate_query('at', translate=True)}")
    print(f"  'KEDİ' -> {translate_query('KEDİ', translate=True)}")
    
    print("🔄 translate_query (translate=False) testi:")
    print(f"  'at' -> {translate_query('at', translate=False)}")
    print(f"  'KEDİ' -> {translate_query('KEDİ', translate=False)}")
    
    print("\n🔍 Doğrudan translate_to_english çağrı testleri:")
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




    """
mapping.py - Türkçe → İngilizce Kelime Eşleştirme Modülü

Tek Sorumluluk Prensibi (SRP):
- Sadece translate=True olduğunda çalışır
- Sadece kelime çevirisi yapar, başka bir sorumluluğu yoktur
"""

# Türkçe → İngilizce sözlük
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
    
    TEK SORUMLULUK: Sadece çeviri yapar.
    - translate=True olduğunda çağrılır
    - Kelimeyi sözlükte arar, bulamazsa aynen döner
    
    Args:
        turkish_word: Türkçe kelime (örn: "at")
    
    Returns:
        İngilizce karşılığı (örn: "horse")
        Eğer kelime sözlükte yoksa, aynen döner.
    """
    cleaned_word = turkish_word.lower().strip()
    return TURKISH_TO_ENGLISH.get(cleaned_word, cleaned_word)


def is_turkish_word(word: str) -> bool:
    """
    Kelimenin Türkçe olup olmadığını kontrol eder.
    
    Basit kontrol: Türkçe karakterler var mı?
    
    Args:
        word: Kontrol edilecek kelime
    
    Returns:
        True eğer Türkçe karakter içeriyorsa
    """
    turkish_chars = "çğıöşüÇĞİÖŞÜ"
    return any(char in turkish_chars for char in word)