from sqlite3 import connect
import os 
import csv 

path_src = "/data/backup"

def load_file(path):

    file = [ ]
    for files in os.listdir(path_src):
        if os.path.isfile(os.path.join(path_src, files)):
            file.append(files)
     
    if not file:
        raise FileNotFoundError("Error aucun fichier trouvé dans le dossier backup")

    dernier_fichier = max(file, key=lambda files: os.path.getmtime(os.path.join(path_src, files)))

    last_file = dernier_fichier.split("_")[0]

    return last_file

def connect_data(filename):
    
    table_name = os.path.splitext(filename)[0]
    db_name = os.path.splitext(filename)[0] + ".db"
    
    csv_path = os.path.join(path_src, filename)
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
        
    connection = connect(db_name)
    cursor = connection.cursor()
   
    
    columns = ", ".join([f'"{col}" TEXT' for col in headers])
    cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})')
    
    insert_data = ", ".join(["?"] * len(headers))
    cursor.executemany(
        f'INSERT INTO "{table_name}" VALUES ({insert_data})',
        rows
    )
    connection.commit()
    
    cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 5')
    preview = cursor.fetchall()
    connection.close()
    print(f" ======== Base de Données {db_name} prete avec la table {table_name} ======== ")
    print("Aperçu des données importées :")
    
    for row in preview:
        print(row)
        
    return db_name, table_name
    
data = load_file(path_src)
db = connect_data(data)

print(f" ======== Base de Données {db} prete ======== ")