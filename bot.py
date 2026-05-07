import requests
import feedparser
import json

WEBHOOK = "PEGA_AQUI_TU_WEBHOOK"
RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=TU_ID"

feed = feedparser.parse(RSS)
video = feed.entries[0]

video_id = video.yt_videoid
title = video.title
link = video.link
thumb = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

try:
    with open("state.json", "r") as f:
        data = json.load(f)
except:
    data = {"last": ""}

if data["last"] != video_id:

    payload = {
        "content": "# 🚨 Nuevo video ferfitos! @everyone",
        "embeds": [
            {
                "title": title,
                "url": link,
                "color": 16711680,
                "image": {"url": thumb},
                "footer": {"text": "Bot automático de YouTube"}
            }
        ]
    }

    requests.post(WEBHOOK, json=payload)

    with open("state.json", "w") as f:
        json.dump({"last": video_id}, f)
