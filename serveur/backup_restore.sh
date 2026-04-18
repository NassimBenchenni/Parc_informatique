#!/bin/bash

# Pour save : bash backup_restore.sh backup
if [ "$1" == "backup" ]; then
    cp data.db backup_data.db
    echo "Sauvegarde terminée : backup_data.db créé."

# Pour restaurer : bash backup_restore.sh restore
elif [ "$1" == "restore" ]; then
    cp backup_data.db data.db
    echo "Restauration terminée : data.db restauré."


else
    echo "Erreur"
fi