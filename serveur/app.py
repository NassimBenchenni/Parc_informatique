from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    try:
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        
        cur.execute("SELECT cles, epo, date, val, quoi, host FROM data ORDER BY epo DESC LIMIT 20")
        historique = cur.fetchall()
        
        cur.execute("SELECT message FROM alertes LIMIT 1")
        alerte = cur.fetchone()
        alerte_msg = alerte[0] if alerte else "Aucune alerte"
        conn.close()
    except Exception as e:
        historique = []
        alerte_msg = "En attente des données..."

    return render_template('index.html', historique=historique, alerte=alerte_msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)