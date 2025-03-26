import threading
import time
import uuid
import json

from collector.cameras import db_utils
from collector.cameras import camera_utils
from collector.config import CONFIG_PATH
from configparser import ConfigParser

# Used to read the .ini configuration file
conf: ConfigParser = ConfigParser()
conf.read(CONFIG_PATH)

def get_plant_infos(index_camera=0):
    photo_id = str(uuid.uuid4())

    # Costruisce dinamicamente le chiavi in base all'indice
    pot_key = f"pot_{index_camera + 1}"  # Gli indici partono da 1 nel file di configurazione
    plant_key = f"plant_{index_camera + 1}"

    # Estrai i dati dai dizionari
    plant_id = json.loads(conf["pots"].get(pot_key, "{}")).get("plant_id")
    plant_status = json.loads(conf["plants"].get(plant_key, "{}")).get("status")

    return {"photo_id": photo_id, "plant_id": plant_id, "status": plant_status}

def collect_photos():
    while True:
        db_utils.ensure_table_exists()
        cameras = camera_utils.list_available_cameras(1)
        plant_info = get_plant_infos()

        # Creiamo e avviamo un thread per ogni elemento nella lista
        threads = []
        for camera_id in range(len(cameras)):
            thread = threading.Thread(target=camera_utils.take_a_photo, args=(plant_info["photo_id"] + str(camera_id),
                                                                        plant_info["status"], 
                                                                        plant_info["plant_id"],
                                                                        camera_id))
            thread.start()
            threads.append(thread)

        # Aspettiamo che tutti i thread terminino
        for thread in threads:
            thread.join()
        
        print("Foto scattate con successo!")
        time.sleep(5)

def define_camera_thread(camera_index=0):
    db_utils.ensure_table_exists()
    cameras = camera_utils.list_available_cameras(camera_index)
    plant_info = get_plant_infos(camera_index)

    camera_utils.take_a_photo(plant_info["photo_id"], plant_info["status"], plant_info["plant_id"], camera_index)
    print("Foto scattata con successo! Camera:", camera_index)
    time.sleep(5)