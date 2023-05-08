"""
Starts the data collection process on the Raspberry Pi. Different threads
are assigned to different sensors and periodically collect the data from them
and send it to the InfluxDB database.

Should be run from the root of the project as: python3 -m collector
"""

from configparser import ConfigParser
import threading
import board

from assets.greenhouse_asset import GreenhouseAsset
from assets.pot_asset import PotAsset
from assets.shelf_asset import ShelfAsset
from sensors.humidity import Humidity
from sensors.light_level import LightLevel
from sensors.mcp3008 import MCP3008
from sensors.moisture import Moisture
from sensors.temperature import Temperature

# We need to use board instead of initializing the pins manually like 'Pin(12)'
# because in this way we have a wrapper that works on every Raspberry Pi model
pinlist = [getattr(board, f"D{i}") for i in range(26)]


def main():
    mcp3008 = MCP3008()

    pin = pinlist[ConfigParser().getint("DHT22", "gpio_pin")]

    # TODO: get channel from config, should we have "moisture_channel1, moisture_channel2, ..."?
    # Should it be a list instead?
    # channel = ConfigParser().getint("MCP3008", "channel")

    shelf_measurement = ShelfAsset(1, Humidity(pin=pin), Temperature(pin=pin))
    thread_shelf = threading.Thread(target=shelf_measurement.read_sensor_data())
    thread_shelf.start()

    pot_measurement = PotAsset(1, "right", "left", "1", Moisture(mcp3008, 1))
    thread_pot = threading.Thread(target=pot_measurement.read_sensor_data())
    thread_pot.start()

    greenhouse_measurement = GreenhouseAsset(LightLevel())
    thread_greenhouse = threading.Thread(
        target=greenhouse_measurement.read_sensor_data()
    )
    thread_greenhouse.start()


if __name__ == "__main__":
    """
    Script to be run on the Raspberry Pi Data Collectors.
    """
    main()
