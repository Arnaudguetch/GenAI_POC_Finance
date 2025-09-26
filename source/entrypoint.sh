#!/bin/bash

set -e

set -x

echo "Lancement des scripts en parallèle..."

echo "Lancement du script ML (main.py)..."
python3 /source/main.py > /logs/main.log 2>&1 &

echo "Lancement du script de sauvegarde des data...."
python3 /data/save_files.py > /logs/save_files.log 2>&1 &

echo "Lancement du script de labase de données..."
python3 /data/database.py > /logs/database.log 2>&1 &

echo "Fin du lancement de tous les scripts..."

wait





