from flask import Flask, request

app = Flask(__name__)

# Remplacez ceci par votre phrase secrète demain
VERIFY_TOKEN = "PJ_2026_Mada" 

@app.route("/", methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Bot PJ opérationnel", 200

@app.route("/", methods=['POST'])
def webhook():
    data = request.get_json()
    print(data) 
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

