#!/bin/bash
cd /home/nassim/nassim/serveur/ || exit

DB_FILE="data.db"

# Création des tables
sqlite3 $DB_FILE "CREATE TABLE IF NOT EXISTS data (cles INTEGER PRIMARY KEY AUTOINCREMENT, epo INTEGER, date TEXT, val REAL, quoi TEXT, host TEXT);"
sqlite3 $DB_FILE "CREATE TABLE IF NOT EXISTS alertes (message TEXT);"

MACHINES=("192.168.56.10" "192.168.56.11" "192.168.56.12")
UTILISATEUR="nassim"

python3 cert_parser.py



for ip in "${MACHINES[@]}"; do
    
    ssh -n $UTILISATEUR@$ip "python3 ~/nassim/sondes/sonde1.py ; bash ~/nassim/sondes/sonde2.sh ; bash ~/nassim/sondes/sonde3.sh" | while IFS=';' read -r quoi host epo val; do
        [ -z "$quoi" ] && continue 
        
        date_str=$(date -d @$epo "+%Y-%m-%d %H:%M:%S")

        sqlite3 $DB_FILE "INSERT INTO data (epo, date, val, quoi, host) VALUES ($epo, '$date_str', $val, '$quoi', '$host');"

        # --- ALERTES ---
        source seuil.config
        if [ "$quoi" == "CPU" ]; then
            alerte=$(echo "$val" | awk -v seuil="$SEUIL_CPU" '{if ($1 > seuil) print 1; else print 0}')
            if [ "$alerte" -eq 1 ]; then
                python3 envoyer_alerte.py "$host" "CPU en surcharge à $val% (Seuil $SEUIL_CPU%)"
            fi
        elif [ "$quoi" == "RAM" ]; then
            alerte=$(echo "$val" | awk -v seuil="$SEUIL_RAM" '{if ($1 > seuil) print 1; else print 0}')
            if [ "$alerte" -eq 1 ]; then
                python3 envoyer_alerte.py "$host" "RAM saturée à $val% (Seuil $SEUIL_RAM%)"
            fi
        elif [ "$quoi" == "DISQUE" ]; then
            alerte=$(echo "$val" | awk -v seuil="$SEUIL_DISQUE" '{if ($1 > seuil) print 1; else print 0}')
            if [ "$alerte" -eq 1 ]; then
                python3 envoyer_alerte.py "$host" "DISQUE saturée à $val% (Seuil $SEUIL_DISQUE%)"
            fi
        fi
    done
done


sqlite3 $DB_FILE "DELETE FROM data WHERE epo <= $(( $(date +%s) - 86400 ));"

python3 generateur_graphiques.py