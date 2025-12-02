def translate_to_tr(text: str) -> str:
    if not text:
        return text
    try:
        r = requests.post(
            "https://libretranslate.com/translate",
            data={
                "q": text,
                "source": "auto",
                "target": "tr",
                "format": "text"
            },
            timeout=5
        )
        return r.json().get("translatedText", text)
    except:
        return text
