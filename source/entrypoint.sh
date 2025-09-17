#!/bin/bash

set -e

echo "Lancement du script ML (main.py)..."
python3 main.py

sleep 4

echo "Démarrage de l'application Streamlit (app.py)..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0



