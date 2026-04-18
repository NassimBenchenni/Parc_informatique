import pygal
import sqlite3

def generer_graphique():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    liste = ['CPU', 'RAM', 'DISQUE', 'PROCESSUS']

    for data in liste:
        cur.execute("SELECT DISTINCT host FROM data WHERE quoi=?", (data,))
        hosts = [row[0] for row in cur.fetchall()]

        if not hosts:
            print(f"Pas encore assez de données pour faire le graphique {data}.")
            continue

        g = pygal.Line(title=f"Évolution : {data}", x_label_rotation=20)
        
        cur.execute("SELECT date FROM data WHERE quoi=? AND host=? ORDER BY epo ASC", (data, hosts[0]))
        labels = [d[0].split(" ")[1] for d in cur.fetchall()]
        g.x_labels = labels

        for host in hosts:
            cur.execute("SELECT val FROM data WHERE quoi=? AND host=? ORDER BY epo ASC", (data, host))
            valeurs = [float(d[0]) for d in cur.fetchall()]
            g.add(host, valeurs)
            
        nom_fichier = f'static/graph_{data}.svg'
        g.render_to_file(nom_fichier)
        print(f"Graphique mis à jour : {nom_fichier}")

    conn.close()

if __name__ == "__main__":
    generer_graphique()