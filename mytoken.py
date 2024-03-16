import json
import requests

user = ''
password = ''
envoy_serial = ''

def get_token():
    # Authentification
    data = {'user[email]': user, 'user[password]': password}
    response = requests.post('http://enlighten.enphaseenergy.com/login/login.json?', data=data)

    if response.status_code == 200:
        response_data = json.loads(response.text)

        if 'session_id' in response_data:
            # Obtenir le jeton
            data = {'session_id': response_data['session_id'], 'serial_num': envoy_serial, 'username': user}
            response = requests.post('http://entrez.enphaseenergy.com/tokens', json=data)

            if response.status_code == 200:
                print(response.text)
                return response.text
            else:
                print(f"La requête pour obtenir le jeton a échoué avec le code d'état {response.status_code}.")
        else:
            print("La clé 'session_id' est manquante dans response_data.")
    else:
        if response.status_code == 401:
            print("Erreur d'authentification. Vérifiez les informations d'identification.")
        else:
            print(f"La requête a échoué avec le code d'état {response.status_code}.")

# Appel de la fonction pour obtenir le jeton
get_token()