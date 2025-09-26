import os 
from datetime import date
import shutil 


def save_csv_files(src, dst="./data/backup"):

    current_date = date.today().strftime("%d-%m-%Y")

    saved_files = []
    for root, dirs, files in os.walk(src):
        for file_name in files:
            if file_name.endswith(".csv"):
                try:
                    src_path = os.path.join(root, file_name)
                    dest_name = f"{file_name}_{current_date}"
                    dst_path = os.path.join(dst, dest_name)
                    shutil.copy2(src_path, dst_path)
                    print(f"Le fichier {file_name} a été copié dans {dst}")
                    saved_files.append(dest_name)
                except Exception as e:
                    print(f"Le fichier {file_name} n'a pas pu être copié : {e}")

    return dst, saved_files


def delete_csv_files(path_src):
    
    deleted_files = []

    for file in os.listdir(path_src):
        file_path = os.path.join(path_src, file)
        if os.path.isfile(file_path) and file.endswith(".csv"):
            os.remove(file_path)
            deleted_files.append(file)
            print(f"Fichier {file} supprimé avec succès du dossier {path_src}.")

    if not deleted_files:
        print("Aucun fichier .csv trouvé à supprimer.")
    else:
        print(f"Total fichiers supprimés : {len(deleted_files)}")


source_path = "./"
backup_dir = "./data/backup"

backup_path, copied_files = save_csv_files(source_path, backup_dir)

print(f"\n======= Sauvegarde terminée dans le dossier : {backup_path} ========")
print("Fichiers copiés :", copied_files)
print()

delete_csv_files(source_path)

    


