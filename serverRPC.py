import csv
import os
from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET

# Charger les données en mémoire
def load_data():
    file_path = "index-egalite-fh-utf8.csv"
    
    # Vérifier si le fichier existe
    if not os.path.isfile(file_path):
        print(f"Erreur: Le fichier {file_path} est introuvable.")
        return []
    
    data = []
    try:
        with open(file_path, newline='', encoding="ISO-8859-1") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            reader.fieldnames = [field.strip() for field in reader.fieldnames]
            
            for row in reader:
                row["SIREN"] = str(row["SIREN"])  # Convertir en string pour éviter les erreurs
                data.append(row)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV: {e}")
        return []
    
    return data

data = load_data()

def dict_to_xml(data_dict):
    """Convertir un dictionnaire en format XML."""
    root = ET.Element("company")
    for key, value in data_dict.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    return ET.tostring(root, encoding="unicode")

def get_company_by_siren(siren):
    """Récupère les informations d'une entreprise par son SIREN et renvoie une réponse en XML."""
    for company in data:
        if company["SIREN"] == str(siren):
            return dict_to_xml(company)  # Convertir en XML
    return "<error>Aucune entreprise trouvée</error>"

# Créer le serveur XML-RPC
def run_server():
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    server.register_function(get_company_by_siren, "get_company_by_siren")

    print("Serveur RPC en cours d'exécution sur le port 8000...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
