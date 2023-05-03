from dataclasses import dataclass
import time
from datetime import datetime

from influxdb_client import Point
from influx.assets.asset import Asset

from influx.influx_controller import InfluxController
from influx.assets.measurement_type import MeasurementType
from sensors.humidity import Humidity
from sensors.temperature import Temperature


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

    def to_point(self) -> Point:
        return (
            Point(MeasurementType.SHELF.get_measurement_name())
            .tag("shelf_floor", self.shelf_floor)
            .field("temperature", self.temperature_sensor.read())
            .field("humidity", self.humidity_sensor.read())
            .time(datetime.now())
        )

    def read_sensor_data(self, interval: int = 5):
        influx_controller = InfluxController()
        bucket = influx_controller.get_bucket(
            "greenhouse"
        ) or influx_controller.create_bucket("greenhouse")

        while True:
            influx_controller.write_point(self.to_point(), bucket)
            print(self.to_point())  # TODO remove
            time.sleep(interval)
