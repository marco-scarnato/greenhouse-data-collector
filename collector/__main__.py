"""
Starts the data collection process on the Raspberry Pi. Different threads
are assigned to different sensors and periodically collect the data from them
and send it to the InfluxDB database.

Should be run from the root of the project as: python3 -m collector
"""
import json
import threading
from sys import argv
from typing import Dict

import board
from adafruit_dht import DHT22

from collector.config import CONFIG_PATH
from collector.demo.demo_influx import demo
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
from collector.assets.plant_asset import PlantAsset
from collector.assets.pot_asset import PotAsset
from collector.assets.shelf_asset import ShelfAsset
from collector.sensors.light_level import LightLevel
from collector.sensors.mcp3008 import MCP3008
from collector.sensors.moisture import Moisture
from collector.sensors.ndvi import NDVI

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

    # Gets switch from config file to enable/disable sensors
    use_infrared_sensor = conf.getboolean("sensor_switches", "use_infrared_sensor")
    use_light_sensor = conf.getboolean("sensor_switches", "use_light_sensor")

    # Initialize InfluxController singleton
    influx_controller = InfluxController()
    influx_controller.create_bucket("greenhouse")

    init_pots_threads()

    init_shelf_thread()

    if use_light_sensor:
        init_greenhouse_thread()

    if use_infrared_sensor:
        init_plants_threads()

    # TODO: method that start a thread which is triggered
    #  if the config file is changed and then restarts all the
    #  asset threads to get the new mapping between assets and sensors


def init_plants_threads():
    """
    Initializes the threads that will read the data from the plants' sensors.
    """
    plants = conf.items("plants")
    # A shared NDVI sensor is used for all the plants in the shelf.
    ndvi = NDVI()
    for _, plant_parameters in plants:
        plant_dict = json.loads(plant_parameters)
        plant_id = plant_dict["plant_id"]
        plant = PlantAsset(plant_id, ndvi)
        thread_plant = threading.Thread(target=plant.read_sensor_data)
        thread_plant.start()


def init_shelf_thread():
    """
    Initializes the threads that will read the data from the shelf's sensors.
    """
    shelves = conf.items("shelves")
    # for now we only have one data-collector per shelf
    shelf_dict: Dict = json.loads(shelves[0][1])

    # In this case temperature and humidity sensors are on the same pin,
    # we can use either of the temperature or humidity gpio_pin on the raspberry
    dht22_gpio_pin = shelf_dict["temperature_gpio_pin"]
    # The DHT22 sensor is used for both temperature and humidity
    # It is initialized with the pin number taken from the configuration file and
    # the pinlist initialized above in order to have a wrapper that works on every Raspberry Pi model
    humidity_temperature_sensor = DHT22(pinlist[int(dht22_gpio_pin)])
    humidity_sensor = Humidity(humidity_temperature_sensor)
    temperature_sensor = Temperature(humidity_temperature_sensor)

    shelf_floor = shelf_dict["shelf_floor"]
    shelf = ShelfAsset(shelf_floor, humidity_sensor, temperature_sensor)
    shelf.set_sensor_read_interval(10)

    thread_shelf = threading.Thread(target=shelf.read_sensor_data)
    thread_shelf.start()


def init_pots_threads():
    """
    Initializes the threads that will read the data from the pots' sensors.
    The moisture sensors are read using the MCP3008 Analog to Digital Converter.
    """
    pots = conf.items("pots")
    for _, pot_parameters in pots:
        pot_dict = json.loads(pot_parameters)
        shelf_floor = pot_dict["shelf_floor"]
        group_position = pot_dict["group_position"]
        pot_position = pot_dict["pot_position"]
        plant_id = pot_dict["plant_id"]
        # The moisture sensors data is converted using a shared MCP3008 Analog to Digital Converter.
        moisture_sensor = Moisture(mcp3008, pot_dict["moisture_adc_channel"])
        pot = PotAsset(
            shelf_floor, group_position, pot_position, plant_id, moisture_sensor
        )
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
    It starts the data collection process if no parameters are passed.
    If the --demo parameter is passed it will run the demo.
    """
    # if argv has a value check it
    if len(argv) > 1:
        # if the first parameter is --demo run the demo
        if argv[1] == "--demo":
            demo()
        else:
            print("Wrong parameter: " + argv[1])
            print("Usage: python3 -m collector [--demo]")
    else:
        main()
