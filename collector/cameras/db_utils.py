import psycopg2

from psycopg2 import OperationalError
from psycopg2 import Binary
from configparser import ConfigParser
from collector.config import CONFIG_PATH

# Used to read the .ini configuration file
conf: ConfigParser = ConfigParser()
conf.read(CONFIG_PATH)

DB_HOST = conf["postgres"]["url"]
DB_PORT = conf["postgres"]["port"]
DB_NAME = conf["postgres"]["name"]
DB_USER = conf["postgres"]["user"]
DB_PASSWORD = conf["postgres"]["pwd"]

def connect_to_postgres():
    """Crea una connessione al database PostgreSQL."""
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connessione a PostgreSQL stabilita con successo!")
        return connection
    except OperationalError as e:
        print(f"Errore durante la connessione a PostgreSQL: {e}")
        return None
    
def ensure_table_exists():
    """Assicura che la tabella 'photos' esista nel database."""
    try:
        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()
            
            # Crea la tabella se non esiste
            create_table_query = """
            CREATE TABLE IF NOT EXISTS photos (
                id VARCHAR PRIMARY KEY,
                photo BYTEA,
                status VARCHAR,
                plant_id VARCHAR
            )
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("Tabella 'photos' verificata/creata con successo!")
            return True
            
    except Exception as e:
        print(f"Errore durante la creazione della tabella: {e}")
        return False
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()
            print("Connessione chiusa")

def post_photo(photo_id, photo_bytes, status="Healty", plant_id="basil"):
    """Inserisce una nuova foto nel database (POST)."""
    try:
        photo_data = Binary(photo_bytes)

        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()
            
            # Controllo se l'ID esiste già
            check_query = "SELECT id FROM photos WHERE id = %s"
            cursor.execute(check_query, (photo_id,))
            
            if cursor.fetchone():
                # Se esiste, aggiorna la foto
                query = "UPDATE photos SET photo = %s, status = %s, plant_id = %s WHERE id = %s"
                cursor.execute(query, (photo_data, status, plant_id, photo_id))
                print(f"Foto con ID '{photo_id}' aggiornata con successo!")
            else:
                # Se non esiste, inserisci una nuova foto
                query = "INSERT INTO photos (id, photo, status, plant_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (photo_id, photo_data, status, plant_id))
                print(f"Foto con ID '{photo_id}' inserita con successo!")
            
            connection.commit()
            return True
            
    except Exception as e:
        print(f"Errore durante l'inserimento della foto: {e}")
        return False
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()
            print("Connessione chiusa")

def get_photo(photo_id):
    """Recupera una foto dal database in base all'ID (GET)."""
    try:
        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()
            
            # Presuppongo che la tabella si chiami 'photos'
            # Modifica il nome della tabella se necessario
            query = "SELECT id, photo, status, plant_id FROM photos WHERE id = %s"
            cursor.execute(query, (photo_id,))
            
            result = cursor.fetchone()
            
            if result:
                id, photo_data, status, plant_id= result
                print(f"Foto con ID '{id}' recuperata con successo!")
                # Restituisce l'ID e i dati binari della foto
                return id, photo_data, status, plant_id
            else:
                print(f"Nessuna foto trovata con ID '{photo_id}'")
                return None
            
    except Exception as e:
        print(f"Errore durante il recupero della foto: {e}")
        return None
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()
            print("Connessione chiusa")

def get_all_status_photo(status):
    """Recupera tutte le foto dal database con questo status (GET)."""
    try:
        connection = connect_to_postgres()
        if connection:
            cursor = connection.cursor()
            
            # Presuppongo che la tabella si chiami 'photos'
            # Modifica il nome della tabella se necessario
            query = "SELECT * FROM photos WHERE status = %s"
            cursor.execute(query, (status,))
            
            results = cursor.fetchall()
            
            if results:
                return results
            else:
                print("Nessuna foto trovata nel database.")
                return []
            
    except Exception as e:
        print(f"Errore durante il recupero della foto: {e}")
        return None
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()
            print("Connessione chiusa")