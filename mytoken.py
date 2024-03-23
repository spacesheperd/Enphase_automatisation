import json
import requests

def get_token(user, password, envoy_serial):
    # Authentification
    data = {'user[email]': user, 'user[password]': password}
    response = requests.post('http://enlighten.enphaseenergy.com/login/login.json?', data=data)

    if response.status_code == 200:
        response_data = json.loads(response.text)

        if 'session_id' in response_data:
            # Obtenir le jeton
            token_data = {'session_id': response_data['session_id'], 'serial_num': envoy_serial, 'username': user}
            token_response = requests.post('http://entrez.enphaseenergy.com/tokens', json=token_data)

            if token_response.status_code == 200:
                print(token_response.text)
                return token_response.text
            else:
                print(f"La requête pour obtenir le jeton a échoué avec le code d'état {token_response.status_code}.")
        else:
            print("La clé 'session_id' est manquante dans response_data.")
    else:
        if response.status_code == 401:
            print("Erreur d'authentification. Vérifiez les informations d'identification.")
        else:
            print(f"La requête a échoué avec le code d'état {response.status_code}.")

# Lecture des informations du fichier JSON
with open("C:/Users/mathi/Desktop/visualstudiocode/minage_script/infos.json", "r") as f:
    json_data = json.load(f)

# Récupération des informations nécessaires
credentials = json_data[0]  # Le premier objet JSON
user = credentials['username']
password = credentials['password']
envoy_serial = credentials['envoy_serial']

# Appel de la fonction pour obtenir le jeton
get_token(user, password, envoy_serial)
