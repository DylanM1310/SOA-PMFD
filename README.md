# DEVOIR SOA sur les API REST et RPC

Groupe : Julian, Dylan, Paul et Mickael

Distribution des données EgaPro en RPC (Vous devez utilisé le fichier rpc.py, pour la notation du RPC) : 


	rpc.py :
		Pour essayer de trouver les informations via un SIREN, utiliser la commande suivante:
			curl -X POST http://localhost:13000/siren -d "NUMERO SIREN"

			

	serverRPC.py :
		Pour essayer de trouver les informations via un SIREN, utiliser la commande suivante:
			curl -X POST http://localhost:8000/siren -d "NUMERO SIREN"




API EgaPro 
Cette API permet de distribuer les données de l'Index EgaPro à partir d'un fichier CSV (index-egalite-fh-utf8.csv). Elle expose un service REST qui retourne les informations associées à un numéro de SIREN donné.

**Prérequis**

Python 3.x

Les dépendances Python suivantes :

- Ballon

- Flask-RESTful

- flacon-swagger-ui


Le code fonctionnel pour cette API est: **apirest-paul.py**

URL Documention : **http://127.0.0.1:5000/swagger/**

 Obtenir les données d'un SIREN : **http://127.0.0.1:5000/siren/423492792 (cliquer sur impression élégante si besoin) cette exemple vous donnera des informations sur DIAVERUM PROVENCE**
