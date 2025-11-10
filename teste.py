import os
from PIL import Image
from PIL import ImageFile

# Permet à PIL de gérer les fichiers tronqués ou partiellement corrompus (utile)
ImageFile.LOAD_TRUNCATED_IMAGES = True 

# Le chemin de votre dossier d'entraînement
base_dir = './images_train' 
# Les sous-dossiers contenant les classes
class_folders = ['Clavier', 'Manette', 'Tasse', 'Verre'] 

print(f"Démarrage de la vérification des fichiers dans {base_dir}...")

files_to_delete = []

for folder_name in class_folders:
    folder_path = os.path.join(base_dir, folder_name)
    print(f"\n-> Vérification du dossier : {folder_name}...")
    
    # Parcourir tous les fichiers dans le dossier
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Ignorer les dossiers ou les fichiers cachés (commence par un point)
        if os.path.isdir(file_path) or filename.startswith('.'):
            continue

        # Vérifier si l'extension est acceptable
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            print(f"❌ NON-IMAGE TROUVÉE : {file_path}")
            files_to_delete.append(file_path)
            continue

        # Tenter d'ouvrir et de charger le fichier (décodage)
        try:
            img = Image.open(file_path)
            img.verify() # Vérifie l'intégrité du fichier
            img.close()
            # print(f"  [OK] {filename}")
            
        except Exception as e:
            # Si une exception est levée, c'est le fichier problématique
            print(f"🛑 ERREUR DE DÉCODAGE (CORRUPTION OU FORMAT INCONNU) : {file_path}")
            print(f"   Détail de l'erreur : {e}")
            files_to_delete.append(file_path)

if files_to_delete:
    print("\n\n--- VÉRIFICATION TERMINÉE ---")
    print("Veuillez supprimer ou renommer les fichiers suivants :")
    for fp in files_to_delete:
        print(f"- {fp}")
else:
    print("\n✅ VÉRIFICATION TERMINÉE : Aucun fichier image corrompu ou au format inconnu n'a été trouvé.")