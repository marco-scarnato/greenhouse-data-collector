import db_utils
import camera_utils
import threading
import time

COUNTER = 0
NUM_CAMERAS = 2

def get_plant_infos():
    global COUNTER
    COUNTER += 1
    return {"photo_id": "photo_" + str(COUNTER), "status": "Healty", "plant_name": "Basil"}

def collect_photos():
    while True:
        db_utils.ensure_table_exists()
        cameras = camera_utils.list_available_cameras(NUM_CAMERAS)
        plant_info = get_plant_infos()

        # Creiamo e avviamo un thread per ogni elemento nella lista
        threads = []
        for camera_id in range(len(cameras)):
            thread = threading.Thread(target=camera_utils.take_a_photo, args=(plant_info["photo_id"] + str(camera_id),
                                                                        plant_info["status"], 
                                                                        plant_info["plant_name"],
                                                                        camera_id))
            thread.start()
            threads.append(thread)

        # Aspettiamo che tutti i thread terminino
        for thread in threads:
            thread.join()
        
        print("Foto scattate con successo!")
        time.sleep(10)