# Enphase_automatisation
Automatisation de consommation d'énergie en utilisant Enphase ainsi que MSI afterburner.

MODIFIER DANS LE infos.json.sample:
- user = ''
- password = ''
- envoy_serial = ''

remarque : trop de tentatives infructueuses pour se connecter avec un token résultera dans un refus d'y accéder pendant un certain temps (time out). La durée du time-out ne dépasse pas 5jours.

Il faut absolument :
- avoir MSI afterburner
- Dans MSI afterburner, mettre 5 profils différents
- renseigner la consommation de ces derniers dans le main.py
- installer les différentes bibliothèques : request, json, subprocess, sys, time

Il est préférable de lancer le programme main.py avec l'aide d'un terminal ou cmd

bonus : trouver un moyen de ne plus devoir faire "autoriser" à chaque changement de profil sur MSI afterburner !
