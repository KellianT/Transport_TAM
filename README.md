# Transport_TAM
Projet_TAM

Bienvenue dans notre programme Python 3 qui vous permettra d'avoir les prochains passages en direct des tramways de Montpellier.

Pour éxécuter le script vous devrez donc saisir dans votre ligne de commande : 

C:\Users\le_chemin_du_programme> Python tam2.py arguments*


Ensuite, plusieurs arguments* seront dont possible : 

L'argument -s vous permettra d'indiquer une station.

L'argument -l vous permettra d'indiquer une ligne.

L'argument -d vous permettra d'indiquer une destination.

L'argument next vous indiquera les prochains départ a la station voulue.

L'argument time vous indiquera les prochains départ d'une station voulue vers la destination voulue.

Voici quelques exemples :
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

C:\Users\le_chemin_du_programme> Python tam2.py next -s COMEDIE

Dans cet exemple l'utilisateur a utiliser l'argument next pour savoir les prochains passages à la station COMEDIE qu'il a définit avec l'argument -s .

VOICI LE RESULTAT :

Ligne 1 vers MOSSON départ dans : 01 min 37 sec
Ligne 1 vers MOSSON départ dans : 10 min 05 sec
Ligne 1 vers MOSSON départ dans : 14 min 46 sec
Ligne 1 vers ODYSSEUM départ dans : 04 min 29 sec
Ligne 1 vers ODYSSEUM départ dans : 16 min 49 sec
Ligne 1 vers ODYSSEUM départ dans : 31 min 08 sec
Ligne 2 vers JACOU départ dans : 02 min 20 sec
Ligne 2 vers JACOU départ dans : 14 min 49 sec
Ligne 2 vers ND DE SABLASSOU départ dans : 26 min 39 sec
Ligne 2 vers SABINES départ dans : 03 min 10 sec
Ligne 2 vers SABINES départ dans : 16 min 43 sec
Ligne 2 vers ST-JEAN DE VEDAS départ dans : 09 min 44 sec

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Dans cet exemple l'utilisateur va utiliser l'argument time pour savoir les prochains passages d'une station voulue avec l'argument -s vers  une destination qu'il aura définit avec l'argument -d .

C:\Users\le_chemin_du_programme> Python tam2.py time -s COMEDIE -l 1 -d MOSSON   

VOICI LE RESULTAT :

Prochain passage de la ligne 1 passant à COMEDIE vers MOSSON départ dans : 02 min 00 
sec
Prochain passage de la ligne 1 passant à COMEDIE vers MOSSON départ dans : 07 min 06 


