import requests
import feedparser
import json
import time
import threading
from flask import Flask
import os

# --- CONFIGURACIÓN ---
WEBHOOK = "https://discord.com/api/webhooks/1502057047980642324/in6bEGxzJEFN9Qx1w1dRBSO8jJ44Bud6NqM4xpKM-tuWy0xnM9j8hgxPL8sPtmYxIGUz"
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCDextee53lOfdcOwlvXvJFg"
INTERVALO = 300  # 5 minutos

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot vivo 🌙", 200

def revisar_youtube():
    while True:
        try:
            feed = feedparser.parse(RSS_URL)
            if feed.entries:
                video = feed.entries[0]
                video_id = video.yt_videoid
                
                # Leer estado
                if os.path.exists("state.json"):
                    with open("state.json", "r") as f:
                        data = json.load(f)
                else:
                    data = {"last": ""}

                if data["last"] != video_id:
                    payload = {
                        "content": "# 🌙🚨-NUEVO VIDEO DISPONIBLE EN YOUTUBE-🌙🚨                             @everyone",
                        "embeds": [{
                            "title": video.title,
                            "url": video.link,
                            "color": 16711680,
                            "image": {"url": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"},
                            "footer": {"text": "By FerfiMoon Stream On Twitch"}
                        }]
                    }
                    requests.post(WEBHOOK, json=payload)
                    with open("state.json", "w") as f:
                        json.dump({"last": video_id}, f)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(INTERVALO)

if __name__ == "__main__":
    threading.Thread(target=revisar_youtube, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
