import os
from datetime import date
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOURCE_DIR = BASE_DIR          
BACKUP_DIR = os.path.join(BASE_DIR, "backup")  

os.makedirs(BACKUP_DIR, exist_ok=True)

def save_csv_files(src=SOURCE_DIR, dst=BACKUP_DIR):
    current_date = date.today().strftime("%d-%m-%Y")
    saved_files = []

    for file_name in os.listdir(src):
        if file_name.lower().endswith(".csv"):
            src_path = os.path.join(src, file_name)
            dest_name = f"{file_name}_{current_date}"
            dst_path = os.path.join(dst, dest_name)
            shutil.copy2(src_path, dst_path)
            print(f"[SAVE] {file_name} → {dst_path}")
            saved_files.append(file_name)

    return dst, saved_files

def delete_csv_files(src=SOURCE_DIR, files_to_delete=None):
    deleted_files = []

    for file_name in files_to_delete or []:
        file_path = os.path.join(src, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            deleted_files.append(file_name)
            print(f"[DELETE] {file_name} supprimé de {src}")

    if not deleted_files:
        print("[DELETE] Aucun fichier à supprimer.")
    else:
        print(f"[DELETE] Total fichiers supprimés : {len(deleted_files)}")


backup_path, copied_files = save_csv_files()
print(f"\n======= Sauvegarde terminée dans : {backup_path} ========")
print("Fichiers copiés :", copied_files)
print()

delete_csv_files(files_to_delete=copied_files)
