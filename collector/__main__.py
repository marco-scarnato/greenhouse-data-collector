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
from adafruit_dht import DHT22

from collector.config import CONFIG_PATH
from collector.influx.influx_controller import InfluxController
from collector.sensors.humidity import Humidity
from collector.sensors.temperature import Temperature

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
from collector.sensors.light_level import LightLevel
from collector.sensors.mcp3008 import MCP3008
from collector.sensors.moisture import Moisture

# We need to use board instead of initializing the pins manually like 'Pin(12)'
# because in this way we have a wrapper that works on every Raspberry Pi model
pinlist = [getattr(board, f"D{i}") for i in range(26)]

# Used to read the .ini configuration file
conf: ConfigParser = ConfigParser()
conf.read(CONFIG_PATH)

# Initialize Analog to Digital Converter (ADC) used to convert analog signal from moisture sensors
mcp3008 = MCP3008()


def main():
    """
    Initialize and starts the threads that will read the data from the sensors and send it to the database.
    The parameters of the sensors and assets are read from the configuration file as specified in the README.
    """

    # Initialize InfluxController singleton
    InfluxController()

    init_pots_threads()

    init_shelf_threads()

    init_greenhouse_thread()

    init_plants_threads()


def init_plants_threads():
    """
    Initializes the threads that will read the data from the plants' sensors.
    """
    plants: List = json.loads(conf["ASSETS"]["plants"])
    # A shared NDVI sensor is used for all the plants in the shelf.
    ndvi = NDVI()
    for plant_dict in plants:
        plant_id = plant_dict['plant_id']
        plant = PlantAsset(plant_id, ndvi)
        thread_plant = threading.Thread(target=plant.read_sensor_data)
        thread_plant.start()


def init_shelf_threads():
    """
    Initializes the threads that will read the data from the shelf's sensors.
    """
    shelf_dict: Dict = json.loads(conf["ASSETS"]["shelf"])
    # In this case temperature and humidity sensors are on the same pin,
    # we can use either of the temperature or humidity gpio_pin on the raspberry
    dht22_gpio_pin = shelf_dict['temperature_gpio_pin']
    # The DHT22 sensor is used for both temperature and humidity
    # It is initialized with the pin number taken from the configuration file and
    # the pinlist initialized above in order to have a wrapper that works on every Raspberry Pi model
    humidity_temperature_sensor = DHT22(pinlist[int(dht22_gpio_pin)])
    humidity_sensor = Humidity(humidity_temperature_sensor)
    temperature_sensor = Temperature(humidity_temperature_sensor)

    shelf_floor = shelf_dict['shelf_floor']
    shelf = ShelfAsset(shelf_floor, humidity_sensor, temperature_sensor)

    thread_shelf = threading.Thread(target=shelf.read_sensor_data, args=(10,))
    thread_shelf.start()


def init_pots_threads():
    """
    Initializes the threads that will read the data from the pots' sensors.
    The moisture sensors are read using the MCP3008 Analog to Digital Converter.
    """
    pots: List = json.loads(conf["ASSETS"]["pots"])
    for pot_dict in pots:
        shelf_floor = pot_dict['shelf_floor']
        group_position = pot_dict['group_position']
        pot_position = pot_dict['pot_position']
        plant_id = pot_dict['plant_id']
        # The moisture sensors data is converted using a shared MCP3008 Analog to Digital Converter.
        moisture_sensor = Moisture(mcp3008, pot_dict['moisture_adc_channel'])
        pot = PotAsset(shelf_floor, group_position, pot_position, plant_id, moisture_sensor)
        thread_pot = threading.Thread(target=pot.read_sensor_data)
        thread_pot.start()


def init_greenhouse_thread():
    """
    Initializes the thread that will read the data from the greenhouse's sensors.
    It will only read the light level.
    """
    light_level = LightLevel()
    greenhouse = GreenhouseAsset(light_level)
    thread_greenhouse = threading.Thread(target=greenhouse.read_sensor_data)
    thread_greenhouse.start()


if __name__ == "__main__":
    """
    Script to be run on the Raspberry Pi Data Collectors.
    """
    main()
