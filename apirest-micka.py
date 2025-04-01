from csv import DictReader
from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

# Read the index-egalite-fh.csv file and store it in a dictionary
egapro_data = {}

# Remplacez 'ISO-8859-1' par l'encodage correct si nécessaire
with open("index-egalite-fh.csv", encoding='ISO-8859-1') as csv:
    reader = DictReader(csv, delimiter=";", quotechar='"')
    for row in reader:
        siren = str(row["SIREN"])  # Convertir en chaîne de caractères
        if egapro_data.get(siren) is None:
            egapro_data[siren] = row
        elif egapro_data[siren]["Année"] < row["Année"]:
            egapro_data[siren].update(row)

application = Flask(__name__)
api = Api(application)

# Swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "EgaPro API"})
application.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

class SirenResource(Resource):
    def get(self, siren):
        """
        Return the EgaPro data for a given SIREN number.
        A 404 is returned if the SIREN is not found.

        ---
        parameters:
          - name: siren
            in: path
            type: integer
            required: true
            description: SIREN number
        responses:
          200:
            description: The corresponding data as a JSON
          404:
            description: SIREN not found
        """
        response = egapro_data.get(str(siren))  # Convertir en chaîne de caractères
        if response is None:
            return {"error": "SIREN not found"}, 404
        return response, 200  # Retourner directement le dictionnaire

api.add_resource(SirenResource, '/siren/<int:siren>')

@application.route("/")
def home():
    return "Welcome to the EgaPro API. Visit /swagger for API documentation."

# A debug flask launcher
if __name__ == "__main__":
    application.run(debug=True)