from flask import Flask, request
import os

app = Flask(__name__)

# Jeton de vérification pour Meta
VERIFY_TOKEN = "PJ_2026_Mada"

@app.route("/webhook", methods=['GET'])
def verify():
    # Facebook envoie des paramètres avec des points (.)
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge, 200
    
    return "Verification failed", 403

@app.route("/webhook", methods=['POST'])
def webhook():
    # Reception des messages
    data = request.get_json()
    print("Données reçues :", data)
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    # Configuration du port pour Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
