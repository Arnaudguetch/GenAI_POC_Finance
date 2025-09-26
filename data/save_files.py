import os 
from datetime import date
import shutil 

SOURCE_DIR = "/data"         
BACKUP_DIR = "/data/backup"


def save_csv_files(src=SOURCE_DIR, dst=BACKUP_DIR):
    
    
    if not os.path.exists(src):
        print(f"Erreur : le dossier source {src} n'existe pas.")
        return dst, []

    if not os.path.exists(dst):
        os.makedirs(dst)
        print(f"Dossier de backup {dst} créé.")

    current_date = date.today().strftime("%d-%m-%Y")
    saved_files = []

    for file_name in os.listdir(src):
        if file_name.lower().endswith(".csv"):
            src_path = os.path.join(src, file_name)
            dest_name = f"{file_name}_{current_date}"
            dst_path = os.path.join(dst, dest_name)
            shutil.copy2(src_path, dst_path)
            print(f"Le fichier {file_name} a été copié dans {dst}")
            saved_files.append(file_name)

    return dst, saved_files


def delete_csv_files(src=SOURCE_DIR, files_to_delete=None):
    if not os.path.exists(src):
        print(f"Erreur : le dossier source {src} n'existe pas.")
        return

    deleted_files = []
    for file_name in files_to_delete or []:
        file_path = os.path.join(src, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            deleted_files.append(file_name)
            print(f"Fichier {file_name} supprimé avec succès du dossier {src}.")

    if not deleted_files:
        print("Aucun fichier à supprimer.")
    else:
        print(f"Total fichiers supprimés : {len(deleted_files)}")
        


backup_path, copied_files = save_csv_files()
print(f"\n======= Sauvegarde terminée dans le dossier {backup_path} ========")
print("Fichiers copiés :", copied_files)
print()

delete_csv_files(files_to_delete=copied_files)

    


