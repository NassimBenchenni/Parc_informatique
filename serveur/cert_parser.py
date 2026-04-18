import requests
from bs4 import BeautifulSoup
import sqlite3

def fetch_cert_alert():
    try:
        url = "https://www.cert.ssi.gouv.fr/alerte/"
        reponse = requests.get(url)
        soup = BeautifulSoup(reponse.content, 'html.parser')
        
        titre_element = soup.find('h3')
            
        derniere_alerte = titre_element.text.strip() if titre_element else "Aucune alerte trouvée sur la page."
        print("Dernière alerte CERT trouvée :", derniere_alerte)
        
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS alertes (message TEXT)')
        cur.execute('DELETE FROM alertes')
        cur.execute('INSERT INTO alertes VALUES (?)', (derniere_alerte,))
        conn.commit()
        conn.close()
        print("Alerte sauvegardée")
        
    except Exception as e:
        print("Erreur lors de la récupération du CERT :", e)

if __name__ == "__main__":
    fetch_cert_alert()