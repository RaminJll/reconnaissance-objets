#!/bin/bash

if [ "$APP_TARGET" = "inference" ]; then
    echo "Lancement du service 'inference'..."
    cd /app/inference
    gunicorn --bind 0.0.0.0:5000 app:app

elif [ "$APP_TARGET" = "transfer_learning" ]; then
    echo "Lancement du service 'transfer_learning'..."
    cd /app/transfer_learning
    gunicorn --bind 0.0.0.0:5000 app:app

else
    echo "Erreur : APP_TARGET '$APP_TARGET' inconnu."
    exit 1
fi