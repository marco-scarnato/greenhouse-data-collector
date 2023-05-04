import threading

from assets.greenhouse_asset import GreenhouseAsset
from assets.pot_asset import PotAsset
from assets.shelf_asset import ShelfAsset
from src.sensors.humidity import Humidity
from sensors.light_level import LightLevel
from src.sensors.mcp3008 import MCP3008
from src.sensors.moisture import Moisture
from src.sensors.temperature import Temperature


def main():
    mcp3008 = MCP3008()

    shelf_measurement = ShelfAsset(1, Humidity(), Temperature())
    thread_shelf = threading.Thread(target=shelf_measurement.read_sensor_data())
    thread_shelf.start()

    pot_measurement = PotAsset(1, 'right', 'left', Moisture(mcp3008, 1))
    thread_pot = threading.Thread(target=pot_measurement.read_sensor_data())
    thread_pot.start()

    greenhouse_measurement = GreenhouseAsset(LightLevel())
    thread_greenhouse = threading.Thread(target=greenhouse_measurement.read_sensor_data())
    thread_greenhouse.start()


if __name__ == '__main__':
    """
    Script to be run on the Raspberry Pi Data Collectors.
    """
    main()
