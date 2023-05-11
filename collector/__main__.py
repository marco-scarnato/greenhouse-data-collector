"""
Starts the data collection process on the Raspberry Pi. Different threads
are assigned to different sensors and periodically collect the data from them
and send it to the InfluxDB database.

Should be run from the root of the project as: python3 -m collector
"""
import json
import threading
from typing import List, Dict

import board

import os

from collector.config import CONFIG_PATH

try:
    # >3.2
    from configparser import ConfigParser
except ImportError:
    # python27
    # Refer to the older SafeConfigParser as ConfigParser
    from configparser import SafeConfigParser as ConfigParser


from collector.assets.greenhouse_asset import GreenhouseAsset
from collector.assets.pot_asset import PotAsset
from collector.assets.shelf_asset import ShelfAsset
from collector.assets.plant_asset import PlantAsset
from collector.sensors.ndvi import NDVI
from collector.sensors.humidity import Humidity
from collector.sensors.light_level import LightLevel
from collector.sensors.mcp3008 import MCP3008
from collector.sensors.moisture import Moisture
from collector.sensors.temperature import Temperature


# We need to use board instead of initializing the pins manually like 'Pin(12)'
# because in this way we have a wrapper that works on every Raspberry Pi model
pinlist = [getattr(board, f"D{i}") for i in range(26)]


def main():
    conf = ConfigParser()
    conf.read(CONFIG_PATH)

    mcp3008 = MCP3008()

    pots: List = json.loads(conf["ASSETS"]["pots"])
    for pot_dict in pots:
        pot = PotAsset(pot_dict, mcp3008)
        thread_pot = threading.Thread(target=pot.read_sensor_data)
        thread_pot.start()

    shelf_dict: Dict = json.loads(conf["ASSETS"]["shelf"])
    shelf = ShelfAsset(shelf_dict)
    thread_shelf = threading.Thread(target=shelf.read_sensor_data)
    thread_shelf.start()

    greenhouse = GreenhouseAsset(LightLevel())
    thread_greenhouse = threading.Thread(target=greenhouse.read_sensor_data)
    thread_greenhouse.start()

    plant = PlantAsset("1", NDVI())
    thread_plant = threading.Thread(target=plant.read_sensor_data)
    thread_plant.start()


if __name__ == "__main__":
    """
    Script to be run on the Raspberry Pi Data Collectors.
    """
    main()
