from mytoken import get_token
import requests
import json
import subprocess
import sys
import time


# Lecture des informations à partir du fichier JSON
with open("infos.json", "r") as f:
    json_data = json.load(f)

# Extraction des informations nécessaires
credentials = json_data[0]
user = credentials['username'] 
password = credentials['password']
url = credentials['url']
temps = int(credentials['temps'])
envoy_serial=credentials['envoy_serial']

#initialisation nombre de profils utilisés 
nombre_profil1 = 0
nombre_profil2 = 0
nombre_profil3 = 0
nombre_profil4 = 0
nombre_profil5 = 0

#définition du nombre de secondes avant de relancer le programme
temps = 60

#definition de l'affichage pour savoir combien de fois les différents profils ont été utilisés
def affichage():
    print("Le profil 1 a été utilisé ", nombre_profil1, "de fois.")
    print("Le profil 2 a été utilisé ", nombre_profil2, "de fois.")
    print("Le profil 3 a été utilisé ", nombre_profil3, "de fois.")
    print("Le profil 4 a été utilisé ", nombre_profil4, "de fois.")
    print("Le profil 5 a été utilisé ", nombre_profil5, "de fois.")

#initialise conso_carte pour la première fois
conso_carte=0

#initialise la consomation des différents profils
conso_profil1=0
conso_profil2=0
conso_profil3=0
conso_profil4=0
conso_profil5=0

token = get_token(user, password, envoy_serial)
while True:
    # Ajouter le token à l'en-tête d'autorisation
    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Effectuer la requête à l'API avec le token dans l'en-tête
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()  # Vérifier les erreurs HTTP

        # Charger la réponse JSON
        data = response.json()

        # Extraire le "wNow" de la deuxième entrée de la liste "consumption" (ce qui nous donne l'exportation d'électricité en temps réel)
        consumption_w_now = data.get("consumption", [])[1].get('wNow', 'N/A')

        #retournerment de variables pour que ça soit positif car flemme de faire des calculs :)
        exporté = consumption_w_now * -1 #donc maintenant si c'est positif ça veut dire qu'il y a exportation d'électricité, si c'est négatif alors c'est importation d'électricité
        print("consommation actuelle :", exporté) #pour check la véritable exportation avant d'y toucher

        #sélectionne la marge de sécurité de consommation en Watt (au cas où il y a un pic d'électricité dans la maison)
        marge=200

        #calcul pour combien ça consomme en prennant en compte la marge et la consommation de la carte graphique (carte graphique ou du système)
        energie = exporté - marge + conso_carte

        #profils MSI afterburner à paramétrer comme on le souhaite avant
        if energie <=150:
            nombre_profil5 = nombre_profil5 + 1
            affichage()
            print(energie, "Profil 5 actuellement activé")
            subprocess.run('"C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe" -profile5', shell=True) #lance le profil 5 (état minimal)
            conso_carte=135

        elif energie > 150 and energie <= 210:
            nombre_profil1 = nombre_profil1 + 1
            affichage()
            print(energie, "Profil 1 actuellement activé")
            subprocess.run('"C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe" -profile1', shell=True) #lance le profil 1 (état très petit)
            conso_carte=150

        elif energie > 210 and energie <=315:
            nombre_profil2 = nombre_profil2 + 1
            affichage()
            print(energie, "Profil 2 actuellement activé")
            subprocess.run('"C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe" -profile2', shell=True) #lance le profil 2 (état petit)
            conso_carte=210

        elif energie > 315 and energie <=370:
            nombre_profil3 = nombre_profil3 + 1
            affichage()
            print(energie, "Profil 3 actuellement activé")
            subprocess.run('"C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe" -profile3', shell=True) #lance le profil 3 (état moyen)
            conso_carte=315

        elif energie > 370:
            nombre_profil4 = nombre_profil3 + 1
            affichage()
            print(energie, "Profil 4 actuellement activé")
            subprocess.run('"C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe" -profile4', shell=True) #lance le profil 4 (état maximal)
            conso_carte=370
    #avoir un retour détaillé sur les erreurs
    except requests.RequestException as e:
        print(f"Une erreur s'est produite lors de la requête HTTP : {e}")
    except json.JSONDecodeError as e:
        print(f"Une erreur s'est produite lors du décodage JSON : {e}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    time.sleep(temps) #relancer le programme toutes les X secondess
