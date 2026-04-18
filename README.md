PROJET DE MONITORING DE PARC INFORMATIQUE
-----------------------------------------

1. DESCRIPTION DU PROJET
Ce projet est une solution complète de surveillance de serveurs Linux. Il se connecte à distance via SSH à différentes machines, récolte leurs métriques matérielles (CPU, RAM, Disque, Processus), stocke l'historique dans une base de données SQLite, génère des graphiques et envoie des alertes par email en cas de surcharge. Il intègre également une veille de sécurité automatique via le CERT-FR.

2. ARCHITECTURE DU PROJET
- /sondes/ : Scripts Python et Bash déployés sur les machines cibles pour lire les métriques matérielles (sonde1.py, sonde2.sh, sonde3.sh).
- serveur.sh : Le coeur du système. Il boucle sur les machines, lance les sondes via SSH et insère les données dans la base SQLite.
- cert_parser.py : Script qui récupère les dernières alertes de sécurité sur le site du CERT-FR.
- generateur_graphiques.py : Génère les graphiques SVG de l'évolution du parc.
- envoyer_alerte.py : Script Python qui envoie un email via Gmail si les seuils d'alerte sont franchis.
- app.py : Interface web (Flask) pour visualiser les graphiques et l'état des serveurs.

3. PRE-REQUIS ET LIBRAIRIES A INSTALLER
Attention, l'installation se divise en deux parties : le serveur principal et les machines surveillées.

SUR LE SERVEUR PRINCIPAL :
Assurez-vous d'avoir Python 3 et SQLite installés :
sudo apt update
sudo apt install python3 python3-pip sqlite3

Installez ensuite les librairies Python nécessaires :
pip3 install python-dotenv flask requests beautifulsoup4 pygal

SUR LES MACHINES CIBLES (A SURVEILLER) :
Le script "sonde1.py" a besoin de la librairie "psutil" pour lire les données du CPU et de la RAM. Sur chaque machine distante, tapez :
sudo apt update
sudo apt install python3 python3-pip
pip3 install psutil

4. CONFIGURATION (A FAIRE AVANT LE PREMIER LANCEMENT)

Etape A : Configuration des Identifiants Gmail (Sécurité)
Créez un fichier nommé ".env" à la racine du dossier "serveur/" contenant :
GMAIL_EMAIL=votre_adresse@gmail.com
GMAIL_PASS=votre_mot_de_passe_d_application
(Utilisez un mot de passe d'application généré depuis les paramètres de sécurité Google, pas votre vrai mot de passe).

Etape B : Configuration des Serveurs Cibles
1. Ouvrez le fichier "serveur.sh".
2. Modifiez le tableau MACHINES avec les adresses IP de vos propres serveurs.
Exemple : MACHINES=("192.168.1.10" "192.168.1.11")
3. Modifiez la variable UTILISATEUR="votre_nom_utilisateur".

Etape C : Configuration des Seuils d'Alerte
Ouvrez le fichier "seuil.config" pour définir à partir de quel pourcentage le système doit envoyer un email.
Exemple :
SEUIL_CPU=85
SEUIL_RAM=90
SEUIL_DISQUE=95

Etape D : Configuration SSH (Indispensable)
Pour que le script serveur.sh se connecte sans demander de mot de passe à chaque fois :
1. Générez une clé sur votre machine principale : ssh-keygen -t ed25519
2. Envoyez la clé sur chaque machine cible : ssh-copy-id utilisateur@192.168.1.10

5. AUTOMATISATION AVEC CRONTAB ET LOGS
Pour que le système tourne tout seul et vérifie les serveurs toutes les 5 minutes :
1. Ouvrez l'éditeur de tâches planifiées en tapant : crontab -e
2. Ajoutez cette ligne tout en bas (en adaptant le chemin absolu selon votre ordinateur) :
*/5 * * * * bash /home/votre_nom/nassim/serveur/serveur.sh >> /home/votre_nom/nassim/serveur/log_serveur.log 2>&1

Cette configuration permet de :
- Lancer le script toutes les 5 minutes (*/5).
- Rediriger la sortie normale et les erreurs dans le fichier "log_serveur.log" (>> ... 2>&1).

6. UTILISATION QUOTIDIENNE

Pour lancer le tableau de bord web :
cd serveur/
python3 app.py
Accédez ensuite à l'interface depuis votre navigateur : http://localhost:5000

Pour surveiller les logs en temps réel (et voir si les sondes tournent bien) :
tail -f /home/votre_nom/nassim/serveur/log_serveur.log
