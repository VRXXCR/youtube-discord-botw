import requests
import feedparser
import json

WEBHOOK = "https://discord.com/api/webhooks/1502057047980642324/in6bEGxzJEFN9Qx1w1dRBSO8jJ44Bud6NqM4xpKM-tuWy0xnM9j8hgxPL8sPtmYxIGUz"
RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCk6mA2TlOmx1K3vbUa5DoPQ"

feed = feedparser.parse(RSS)
video = feed.entries[0]

video_id = video.yt_videoid
title = video.title
link = video.link
thumb = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

# fallback si falla
fallback_thumb = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

# cargar estado
try:
    with open("state.json", "r") as f:
        data = json.load(f)
except:
    data = {"last": ""}

# si es nuevo video
if data["last"] != video_id:

    payload = {
        "content": "# 🌙🚨 Nuevo Videos Ferfitos @everyone",
        "embeds": [
            {
                "title": title,
                "url": link,
                "color": 16711680,
                "image": {"url": thumb},
                "footer": {"text": "By FerfiMoon Stream On Twitch"}
            }
        ]
    }

    requests.post(WEBHOOK, json=payload)

    # guardar nuevo estado
    with open("state.json", "w") as f:
        json.dump({"last": video_id}, f)
