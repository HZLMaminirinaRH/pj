from flask import Flask, request
import os, random, requests
from pymongo import MongoClient

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
collection = client["pj_db"]["pj"]

def send_message(sender_id, text):
    url = f"https://graph.facebook.com/v19.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": text}
    }
    requests.post(url, params=params, json=payload)

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge, 200
    return "Erreur Token", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                if event.get("message"):
                    sender_id = event["sender"]["id"]
                    try:
                        count = collection.count_documents({})
                        if count > 0:
                            index = random.randint(0, count - 1)
                            fragment = list(collection.find().limit(1).skip(index))[0]
                            paragraphes = fragment.get("paragraphes", [])
                            texte = " ".join(paragraphes) if paragraphes else "Fragment introuvable."
                            send_message(sender_id, texte)
                    except Exception as e:
                        print(f"Erreur : {e}")
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
