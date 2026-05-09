from flask import Flask, request
import os
import random
from pymongo import MongoClient

app = Flask(__name__)

# --- CONFIGURATION ---
VERIFY_TOKEN = "PJ_2026_Mada"

# Ton adresse complète mise à jour (Remplace bien <user_password>)
MONGO_URI = "mongodb://rahajarisonahmaminirina_db_user:<SYGq8Gzmk5S7rQCE>@ac-wqfc2fe-shard-00-00.3lc6oso.mongodb.net:27017,ac-wqfc2fe-shard-00-01.3lc6oso.mongodb.net:27017,ac-wqfc2fe-shard-00-02.3lc6oso.mongodb.net:27017/?ssl=true&replicaSet=atlas-4uvhfd-shard-0&authSource=admin&appName=Cluster0"

# Connexion à MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client.pj_db
collection = db.pj

@app.route("/webhook", methods=['GET'])
def verify():
    # Vérification exigée par Meta
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge, 200
    return "Erreur Token", 403

@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.get_json()
    
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    
                    # Logique : Tirer un fragment au sort dans ta base de 634 textes
                    try:
                        count = collection.count_documents({})
                        if count > 0:
                            random_index = random.randint(0, count - 1)
                            fragment = list(collection.find().limit(1).skip(random_index))[0]
                            # On récupère le texte (assure-toi que le champ s'appelle 'texte' dans Atlas)
                            texte_a_envoyer = fragment.get("texte", "Fragment trouvé mais champ 'texte' absent.")
                            print(f"Prêt à envoyer à {sender_id}: {texte_a_envoyer}")
                        else:
                            print("La collection est vide.")
                    except Exception as e:
                        print(f"Erreur MongoDB : {e}")
                        
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
