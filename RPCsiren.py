import csv
from flask import Flask, request, jsonify

app = Flask(name)

csv_file_path = r"C:\Users\Paul\Desktop\SOA\index-egalite-fh-utf8.csv"
siren_data = {}

try:
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            siren = row["SIREN"].strip()
            siren_data[siren] = {
                "SIREN": siren,
                "Raison Sociale": row.get("Raison Sociale", "").strip()
            }
except Exception as e:
    print("Erreur lors du chargement du fichier CSV:", e)
    exit(1)

print("SIREN chargés :", list(siren_data.keys())[:10])
print("Colonnes du CSV :", reader.fieldnames)

@app.route("/siren", methods=["POST"])
def get_siren():
    # Décodage et nettoyage de la donnée reçue
    siren = request.data.decode("utf-8").strip()
    # Supprimer d'éventuels guillemets autour de la valeur
    if siren.startswith('"') and siren.endswith('"'):
        siren = siren[1:-1]
    print(f"Requête POST reçue pour SIREN: {repr(siren)}")
    data = siren_data.get(siren)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "SIREN non trouvé"}), 404

if name == "main":
    print("Démarrage du serveur sur le port 13000...")
    app.run(host="0.0.0.0", port=13000)