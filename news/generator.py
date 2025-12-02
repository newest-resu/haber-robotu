import os
import json
from datetime import datetime
import re
import requests
import xml.etree.ElementTree as ET

os.makedirs("news", exist_ok=True)

RSS_SOURCES = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.hurriyet.com.tr/rss/anasayfa",
    "https://www.cnnturk.com/feed/rss/all/news",
]

def clean_html(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"<.*?>", " ", text).replace("&nbsp;", " ").strip()

def extract_image(item):
    # 1. media:content
    media = item.find("{http://search.yahoo.com/mrss/}content")
    if media is not None and "url" in media.attrib:
        return media.attrib["url"]

    # 2. media:thumbnail
    thumb = item.find("{http://search.yahoo.com/mrss/}thumbnail")
    if thumb is not None and "url" in thumb.attrib:
        return thumb.attrib["url"]

    # 3. enclosure
    enclosure = item.find("enclosure")
    if enclosure is not None and "url" in enclosure.attrib:
        return enclosure.attrib["url"]

    # 4. description içinden <img> ara
    desc = item.findtext("description") or ""
    img = re.search(r'<img[^>]+src="([^"]+)"', desc)
    if img:
        return img.group(1)

    return ""

articles = []

for src in RSS_SOURCES:
    try:
        print("Kaynak:", src)
        resp = requests.get(src, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        root = ET.fromstring(resp.content)

        items = root.findall(".//item")
        for item in items[:20]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            desc = item.findtext("description") or ""
            summary = clean_html(desc)

            if not title or not link:
                continue

            image = extract_image(item)

            articles.append({
                "title": title,
                "summary": summary,
                "image": image,
                "url": link
            })

    except Exception as e:
        print("Hata:", src, e)

output = {
    "generated_at": datetime.utcnow().isoformat(),
    "articles": articles
}

with open("news/latest.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("TOPLAM HABER:", len(articles))
