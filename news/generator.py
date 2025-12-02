def translate_to_tr(text: str) -> str:
    if not text:
        return text
    try:
        r = requests.post(
            "https://libretranslate.de/translate",
            json={
                "q": text,
                "source": "auto",
                "target": "tr",
                "format": "text"
            },
            headers={"Content-Type": "application/json"},
            timeout=8
        )
        return r.json().get("translatedText", text)
    except Exception as e:
        print("Çeviri hatası:", e)
        return text
