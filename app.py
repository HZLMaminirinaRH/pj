from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = "PJ_2026_Mada"

@app.route("/webhook", methods=['GET'])
def verify():
    # Facebook envoie hub.verify_token et hub.challenge
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if token_sent == VERIFY_TOKEN:
        return challenge
    return "Token incorrect", 403

@app.route("/webhook", methods=['POST'])
def webhook():
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
