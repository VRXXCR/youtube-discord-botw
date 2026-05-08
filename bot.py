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
    return "Bot de FerfiMoon está vivo y vigilando 🌙", 200

def revisar_youtube():
    # Esta variable evita que el bot mande el último video apenas se enciende
    primera_ejecucion = True
    print("Iniciando bucle de revisión en segundo plano...")

    while True:
        try:
            feed = feedparser.parse(RSS_URL)
            if feed.entries:
                video = feed.entries[0]
                video_id = video.yt_videoid
                
                # Intentar leer el estado guardado
                if os.path.exists("state.json"):
                    with open("state.json", "r") as f:
                        try:
                            data = json.load(f)
                        except:
                            data = {"last": ""}
                else:
                    data = {"last": ""}

                # LÓGICA DE CONTROL
                if primera_ejecucion:
                    # Al arrancar (o actualizar), marcamos el video actual como 'visto'
                    print(f"Sincronizando: Marcando video {video_id} como último visto.")
                    with open("state.json", "w") as f:
                        json.dump({"last": video_id}, f)
                    primera_ejecucion = False
                
                elif data["last"] != video_id:
                    # Si ya pasó la primera revisión y el ID cambia, es un video nuevo real
                    print(f"¡NUEVO VIDEO DETECTADO!: {video.title}")
                    
                    payload = {
                        "content": "# 🌙🚨 Nuevo Video de Ferfi @everyone",
                        "embeds": [{
                            "title": video.title,
                            "url": video.link,
                            "color": 16711680,
                            "image": {"url": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"},
                            "footer": {"text": "By FerfiMoon Stream On Twitch"}
                        }]
                    }
                    
                    res = requests.post(WEBHOOK, json=payload)
                    if res.status_code in [200, 204]:
                        with open("state.json", "w") as f:
                            json.dump({"last": video_id}, f)
                else:
                    print("Revisado: No hay videos nuevos.")

        except Exception as e:
            print(f"Error en la revisión: {e}")
        
        time.sleep(INTERVALO)

if __name__ == "__main__":
    # Iniciar el bot en un hilo para que no bloquee a Flask
    threading.Thread(target=revisar_youtube, daemon=True).start()
    
    # Render asigna un puerto dinámico, lo tomamos de las variables de entorno
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
