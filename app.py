from flask import Flask, request
import os
from pymongo import MongoClient

app = Flask(__name__)

# --- CONFIGURATION ---
VERIFY_TOKEN = "PJ_2026_Mada"

# REMPLACE la ligne ci-dessous par ton "Connection String" MongoDB Atlas
MONGO_URI = "ton_lien_mongodb_atlas_ici"

# Connexion à la base de données
client = MongoClient(MONGO_URI)
db = client.pj_database  # Remplace par le nom de ta base si différent
collection = db.fragments_livre  # Remplace par le nom de ta collection

@app.route("/webhook", methods=['GET'])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Erreur Token", 403

@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Logique pour extraire un fragment aléatoire de ton livre
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if messaging_event.get("message"):
                    # Ici on pourrait chercher un fragment dans MongoDB
                    # fragment = collection.find_one() 
                    print("Message reçu, prêt à interroger MongoDB")
                    
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
