import os 
from datetime import date
import shutil 


def save_file(src, dst):
    
    current_date = date.today().strftime("%d-%m-%Y")
    dst = "./backup"
    os.makedirs(dst, exist_ok=True)
    
    saved_files = []
    for root, dirs, files in os.walk(src):
        for file_name in files:
            try:
                if file_name.endswith(".csv"):
                    src_path = os.path.join(root, file_name)
                    dest_name = f"{file_name}_{current_date}"
                    dst_path = os.path.join(dst, dest_name)
                    shutil.copy2(src_path, dst_path)
                    print(f"Le fichier {file_name} est present dans le dossier data")
                    saved_files.append(dest_name) 
            except:
                print(f"Le {file_name} ignoré (pas un .csv ou déjà dans le backup)")
                
                
    return dst, saved_files

source_path = "./"
backup_dir = "./backup/"               
backup_path, copied_files = save_file(source_path, backup_dir)

print(f"\n ======= Sauvegarde terminée dans le dossier : {backup_path} ========")
print("Fichiers copiés :", copied_files)
print()

def delete_file(path_src):
    
    deleted_file = []
    for file in os.listdir(path_src):
        file_path = os.path.join(path_src, file)
        if os.path.isfile(file_path) and file.endswith(".csv"):
            os.remove(file_path)
            deleted_file.append(file)
            print(f"Fichier {file} supprimé avec succés du dossier data.")
            
    if not deleted_file:
        print("Aucun fichier .csv trouvé dans le dossier.")
    else:
        print(f"Total fichiers supprimés : {len(deleted_file)}")

delete_src = "./"
delete_file(delete_src)

     


    


