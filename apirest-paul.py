from csv import DictReader
from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

# Dictionnaire pour stocker les données de l'Index EgaPro, avec le SIREN comme clé
egapro_data = {}

# Ouverture et lecture du fichier CSV "index-egalite-fh-utf8.csv" avec l'encodage UTF-8
with open("index-egalite-fh-utf8.csv", encoding='utf-8') as csv_file:
    # Initialisation du DictReader pour lire le CSV en utilisant ";" comme séparateur
    reader = DictReader(csv_file, delimiter=";", quotechar='"')
    # Parcours de chaque ligne du CSV
    for row in reader:
        # Nettoyage des clés : suppression des espaces superflus au début et à la fin
        row = {key.strip(): value for key, value in row.items()}
        
        # Vérification que les colonnes essentielles "SIREN" et "Année" existent
        if "SIREN" not in row or "Année" not in row:
            continue  # Passage à la ligne suivante si l'une des colonnes est absente
        
        # Extraction et nettoyage du numéro de SIREN (conversion en chaîne de caractères et suppression des espaces)
        siren = str(row["SIREN"]).strip()
        
        # Mise à jour du dictionnaire :
        # Si le SIREN n'est pas encore présent, on ajoute la ligne
        if siren not in egapro_data:
            egapro_data[siren] = row
        else:
            # Si le SIREN existe déjà, on compare les années pour conserver la ligne la plus récente
            try:
                current_year = int(egapro_data[siren]["Année"])
                new_year = int(row["Année"])
            except ValueError:
                # En cas d'erreur de conversion, comparer en tant que chaînes
                current_year = egapro_data[siren]["Année"]
                new_year = row["Année"]
            # Mise à jour si la nouvelle ligne a une année supérieure
            if new_year > current_year:
                egapro_data[siren] = row

# Initialisation de l'application Flask
application = Flask(__name__)
# Création de l'API REST avec Flask-RESTful
api = Api(application)

# Configuration de Swagger pour générer la documentation de l'API
SWAGGER_URL = '/swagger'         # URL où l'interface Swagger sera accessible
API_URL = '/static/swagger.json'  # Chemin vers le fichier swagger.json contenant la description de l'API
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "EgaPro API"}  # Nom affiché dans l'interface Swagger
)
# Enregistrement de la blueprint Swagger dans l'application Flask
application.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Définition de la ressource pour accéder aux données par SIREN
class SirenResource(Resource):
    def get(self, siren):
        """
        Retourne les données EgaPro pour un numéro de SIREN donné.
        Renvoie un code 404 si le SIREN n'est pas trouvé.
        """
        # Récupération des données correspondant au SIREN
        response = egapro_data.get(str(siren))
        if response is None:
            # Retour d'une erreur 404 si le SIREN n'existe pas dans le dictionnaire
            return {"error": "SIREN not found"}, 404
        # Retour des données avec un code 200 en cas de succès
        return response, 200

# Ajout de la ressource SirenResource à l'API, accessible via l'URL /siren/<int:siren>
api.add_resource(SirenResource, '/siren/<int:siren>')

# Définition d'une route simple pour la page d'accueil
@application.route("/")
def home():
    return "Welcome to the EgaPro API. Visit /swagger for API documentation."

# Lancement du serveur Flask en mode debug
if __name__ == "__main__":
    application.run(debug=True)
