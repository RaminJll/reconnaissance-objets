# 👁️ Reconnaissance d'Objets via Webcam (MobileNetV2)

Application web interactive capable d'identifier des objets en temps réel via la webcam. L'intelligence artificielle analyse le flux vidéo et affiche l'objet détecté avec un pourcentage de confiance.

Le projet utilise **MobileNetV2** et propose deux modes de fonctionnement distincts :

1.  **Inférence (Standard) :** Utilise le modèle pré-entraîné sur ImageNet (1000 classes d'objets génériques).
2.  **Transfer Learning (Spécialisé) :** Utilise un modèle ré-entraîné spécifiquement pour détecter 4 objets : **Clavier, Manette, Tasse, Verre**.

---

## 🛠 Technologies

* **Backend :** Python 3.9+, Flask, Gunicorn
* **IA / Deep Learning :** TensorFlow, Keras, MobileNetV2
* **Frontend :** HTML5, JavaScript (Capture Webcam)
* **Déploiement :** Docker (Multi-target entrypoint)

## 📂 Structure du Projet

```text
C:.
|   .gitattributes
|   Dockerfile
|   entrypoint.sh
|   requirements.txt
|   structure.txt
|   
+---inference             # Mode standard (1000 classes)
|   |   app.py
|   |   model.py
|   |   mon_modele.keras
|   |   
|   +---static
|   |       camera.js
|   |       
|   \---templates
|           index.html
|           
\---transfer_learning     # Mode spécialisé (4 classes)
    |   app.py
    |   model.py
    |   mon_modele.keras
    |   
    +---images_train      # Données d'entraînement
    |   +---Clavier
    |   +---Manette
    |   +---Tasse
    |   \---Verre
    |           
    +---static
    |       camera.js
    |       
    \---templates
            index.html
```
---

## 🐳 Utilisation avec Docker

L'image Docker contient les deux applications. Utilisez la variable APP_TARGET pour choisir le mode et le mapping de port (-p) pour choisir l'adresse d'accès.

1. **Construire l'image**
   ```bash
    docker build -t web-recon-app .
    ```
2.  **Mode "Inférence" (Port 5000)**
   Détection d'objets génériques (1000 classes).
    ```bash
    docker run -it --rm -p 5000:5000 -e APP_TARGET=inference web-recon-app
    ```
    👉 Accès : http://localhost:5000

4.  **Mode "Transfer Learning" (Port 5001)**
   Détection spécialisée (Clavier, Manette, Tasse, Verre).
    ```bash
    docker run -it --rm -p 5001:5000 -e APP_TARGET=transfer_learning web-recon-app
    ```
    👉 Accès : http://localhost:5001

---

## 🚀 Lancement Local

Si vous souhaitez lancer l'application directement sur votre machine sans conteneurisation :

1. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
    ```
2. **Lancer le mode de votre choix :**
  * **Inférence :**
     ```bash
     cd inference
     python app.py
     ```
  * **Transfer Learning :**
     ```bash
     cd transfer_learning
     python app.py
     ```

## ⚠️ Note Importante

Assurez-vous que le fichier entrypoint.sh est bien sauvegardé au format LF (Line Feed) et non CRLF. Le fichier .gitattributes inclus dans ce projet gère cela automatiquement.
