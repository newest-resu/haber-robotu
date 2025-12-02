import requests
import json
import os
from datetime import datetime

os.makedirs("news", exist_ok=True)

API = "https://newsapi.org/v2/top-headlines?country=tr&apiKey=4c9f0d2d6b4a40d98c98a566da21a79f"

data = requests.get(API).json()

articles = []

for item in data.get("articles", []):
    articles.append({
        "title": item.get("title", ""),
        "summary": item.get("description", ""),
        "image": item.get("urlToImage", ""),
        "url": item.get("url", "")
    })

output = {
    "generated_at": str(datetime.utcnow()),
    "articles": articles
}

with open("news/latest.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
