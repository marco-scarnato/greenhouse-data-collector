from configparser import ConfigParser
from collector.config import CONFIG_PATH

from urllib.parse import urljoin

import requests

# Used to read the .ini configuration file
config_file: ConfigParser = ConfigParser()
config_file.read(CONFIG_PATH)

API_HOST = config_file["api"]["url"]
API_PORT = config_file["api"]["port"]
API_BASE = f"http://{API_HOST}:{API_PORT}/"
API_BASE = urljoin(API_BASE, config_file["api"]["base"])


## API ##
def get_plant(plant_id):
    api_get_path = API_BASE + "/" + str(plant_id)
    response = requests.get(api_get_path)
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code

def get_plants():
    response = requests.get(API_BASE)
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code

def patch_plant(plant_id, current_status, new_status):
    print(f"PATCH: {plant_id} in {current_status} -> {new_status}")
    api_patch_path = urljoin(API_BASE, str(plant_id))
    response = requests.patch(api_patch_path, data={'statusNew': new_status})
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code