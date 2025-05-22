import threading
import time
import json

from collector.cameras import utils_database
from collector.cameras import utils_camera
from collector.cameras import utils_api

from collector.config import CONFIG_PATH
from configparser import ConfigParser

# Load configuration from .ini file
conf: ConfigParser = ConfigParser()
conf.read(CONFIG_PATH)

def thread_take_photos(cam_left_id, cam_right_id):
    """
    Background thread that continuously captures photos from two cameras (left and right)
    using configuration data to determine plant ID and status.

    Args:
        cam_left_id (int): Index of the left camera.
        cam_right_id (int): Index of the right camera.
    """
    utils_database.ensure_table_exist()

    while True:
        try:
            # Get config values for the left plant
            pot_key_left = "pot_1"
            plant_key_left = "plant_1"

            plant_id_left = json.loads(conf["pots"].get(pot_key_left, "{}")).get("plant_id")
            plant_status_left = utils_api.get_plant(plant_id_left)["status"]

            print(f"INFO.1 = Taking photo for LEFT plant_id={plant_id_left}, status={plant_status_left}")
            utils_camera.take_a_photo(plant_status_left, plant_id_left, cam_left_id)

        except Exception as e:
            print(f"ERROR.1 = LEFT camera failed: {e}")

        try:
            # Get config values for the right plant
            pot_key_right = "pot_2"
            plant_key_right = "plant_2"

            plant_id_right = json.loads(conf["pots"].get(pot_key_right, "{}")).get("plant_id")
            plant_status_right = utils_api.get_plant(plant_id_right)["status"]

            print(f"INFO.2 = Taking photo for RIGHT plant_id={plant_id_right}, status={plant_status_right}")
            utils_camera.take_a_photo(plant_status_right, plant_id_right, cam_right_id)

        except Exception as e:
            print(f"ERROR.2 = RIGHT camera failed: {e}")

        print("INFO.3 = Waiting before taking next photos...")
        time.sleep(3600) # 1h