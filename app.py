from flask import Flask, request
import os

app = Flask(__name__)

# Ton jeton exact (attention aux majuscules/minuscules)
VERIFY_TOKEN = "PJ_2026_Mada"

@app.route("/webhook", methods=['GET'])
def verify():
    # Facebook utilise des points (.) dans ses requêtes
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIE")
        return challenge, 200
    
    return "Erreur de validation", 403

@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.get_json()
    print("Message reçu :", data)
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    # Railway utilise la variable d'environnement PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
