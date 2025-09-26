import os 
from datetime import date
import shutil 


def save_csv_files(src="./data", dst="./data/backup"):
    
    
    if not os.path.exists(src):
        print(f"Erreur : le dossier source {src} n'existe pas.")
        return dst, []

    if not os.path.exists(dst):
        print(f"Erreur : le dossier de backup {dst} n'existe pas.")
        return dst, []

    current_date = date.today().strftime("%d-%m-%Y")
    saved_files = []

    for file_name in os.listdir(src):
        if file_name.lower().endswith(".csv"):
            src_path = os.path.join(src, file_name)
            dest_name = f"{file_name}_{current_date}"
            dst_path = os.path.join(dst, dest_name)
            try:
                shutil.copy2(src_path, dst_path)
                print(f"Le fichier {file_name} a été copié dans {dst}")
                saved_files.append(file_name)
            except Exception as e:
                print(f"Impossible de copier {file_name} : {e}")

    return dst, saved_files



def delete_csv_files(src="./data", files_to_delete=None):
   
   
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
        


source_path = "./data"         
backup_dir = "./data/backup" 

backup_path, copied_files = save_csv_files(source_path, backup_dir)

print(f"\n======= Sauvegarde terminée dans le dossier : {backup_path} ========")
print("Fichiers copiés :", copied_files)

delete_csv_files(source_path, copied_files)

    


