#!/bin/bash
set -e
set -x

mkdir -p /logs

echo "=== Lancement de main.py (ML) ==="
python3 /source/main.py > /logs/main.log 2>&1

CSV_FILE="/data/clients.csv"
TIMEOUT=30   
ELAPSED=0

while [ ! -f "$CSV_FILE" ]; do
    sleep 1
    ELAPSED=$((ELAPSED+1))
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "Erreur : le fichier $CSV_FILE n'a pas été généré dans $TIMEOUT secondes."
        exit 1
    fi
done

echo "=== Lancement de save_files.py (sauvegarde) ==="
python3 /data/save_files.py > /logs/save_files.log 2>&1

echo "=== Lancement de database.py ==="
python3 /data/database.py > /logs/database.log 2>&1

echo "=== Tous les scripts ont été exécutés avec succès ==="

