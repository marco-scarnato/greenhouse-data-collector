from dataclasses import dataclass
import time
from typing import Dict

from influxdb_client import Point
from collector.assets.asset import Asset
from collector.assets.measurement_type import MeasurementType

from collector.influx.influx_controller import InfluxController
from collector.sensors.humidity import Humidity
from collector.sensors.temperature import Temperature


@dataclass
class ShelfAsset(Asset):
    """
    Class representing The Shelf Asset

    Attributes
    ----------
    shelf_floor: int
        (tag) floor of the shelf, can be 1 or 2
    humidity_sensor: Humidity
        humidity sensor
    temperature_sensor: Temperature
        temperature sensor
    """
    shelf_floor: int
    humidity_sensor: Humidity
    temperature_sensor: Temperature

    def __post_init__(self):
        if self.shelf_floor != 1 and self.shelf_floor != 2:
            raise ValueError("shelf_floor must be 1 or 2")

    def __init__(self, shelf_dict: Dict):
        self.shelf_floor = shelf_dict['shelf_floor']
        self.humidity_sensor = Humidity(pin=shelf_dict['humidity_gpio_pin'])
        self.temperature_sensor = Temperature(pin=shelf_dict['temperature_gpio_pin'])
        self.influx_controller = InfluxController()

    def to_point(self) -> Point:
        return (
            Point(MeasurementType.SHELF.get_measurement_name())
            .tag("shelf_floor", self.shelf_floor)
            .field("temperature", self.temperature_sensor.read())
            .field("humidity", self.humidity_sensor.read())
        )

    def read_sensor_data(self, interval: int = 5):
        influx_controller = InfluxController()
        bucket = influx_controller.get_bucket("greenhouse")

        while True:
            point = self.to_point()
            print(point)
            influx_controller.write_point(point, bucket)
            time.sleep(interval)
