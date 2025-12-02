import urllib.parse

def translate_to_tr(text: str) -> str:
    if not text:
        return text
    try:
        query = urllib.parse.quote(text)
        url = f"https://api.mymemory.translated.net/get?q={query}&langpair=en|tr"
        r = requests.get(url, timeout=10)
        data = r.json()
        translated = data.get("responseData", {}).get("translatedText")
        return translated or text
    except Exception as e:
        print("Çeviri hatası:", e)
        return text
