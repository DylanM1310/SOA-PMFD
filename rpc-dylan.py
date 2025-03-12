import csv
from jsonrpcserver import method, serve, dispatch
from flask import Flask, request, jsonify

app = Flask(__name__)

# Chargement des données dans un dictionnaire
siren_data = {}
with open("/Users/dylan/Documents/index-egalite-fh-utf8.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        siren = row["SIREN"].strip()
        if siren not in siren_data:
            siren_data[siren] = {"SIREN": row["SIREN"].strip()} #"Raison Sociale": row["Raison Sociale"].strip()}

# Afficher quelques SIREN pour vérification
print("SIREN chargés:", list(siren_data.keys())[:10])
print("")
print("🧐 Aperçu des colonnes du fichier CSV :", reader.fieldnames)

# Définition de la méthode JSON-RPC
@method
def get_data_by_siren(siren: str):
    print(f"Requête reçue pour SIREN: {siren}")  # Debug
    siren = siren.strip()  # Nettoyage
    data = siren_data.get(siren)
    if data:
        return data
    else:
        return {"error": "SIREN non trouvé"}

# Route alternative permettant d'envoyer uniquement un SIREN en requête HTTP POST
@app.route("/siren", methods=["POST"])
def get_siren():
    siren = request.data.decode("utf-8").strip()
    print(f"Requête POST reçue pour SIREN: {siren}")  # Debug
    data = siren_data.get(siren)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "SIREN non trouvé"}), 404

if __name__ == "__main__":
    print("Démarrage du serveur JSON-RPC sur le port 13000...")
    app.run(host="0.0.0.0", port=13000)
