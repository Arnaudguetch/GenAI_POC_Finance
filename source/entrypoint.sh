#!/bin/bash

set -e

set -x

echo "Lancement du script ML (main.py)..."
python3 /source/main.py &

echo "Fin du lancement de main.py..."

echo "Lancement du script de sauvegarde des data...."
python3 /data/save_files.py &

echo "Lancement du script de labase de données..."
python3 /data/database.py &

echo "Fin du lancement de tous les scripts..."

wait





