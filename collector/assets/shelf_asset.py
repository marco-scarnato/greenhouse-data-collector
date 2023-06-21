from dataclasses import dataclass

from influxdb_client import Point

from collector.assets.asset import Asset
from collector.assets.measurement_type import MeasurementType
from collector.sensors.humidity import Humidity
from collector.sensors.temperature import Temperature


@dataclass
class ShelfAsset(Asset):
    """
    Class representing The Shelf Asset

    Attributes:
        shelf_floor (str): floor of the shelf, can be 1 or 2
        humidity_sensor (Humidity)
        temperature_sensor (Temperature)
    """

    shelf_floor: str
    humidity_sensor: Humidity
    temperature_sensor: Temperature

    def __post_init__(self):
        if self.shelf_floor != "1" and self.shelf_floor != "2":
            raise ValueError("shelf_floor must be 1 or 2")

    def to_point(self) -> Point:
        return (
            Point(MeasurementType.SHELF.get_measurement_name())
            .tag("shelf_floor", self.shelf_floor)
            .field("temperature", self.temperature_sensor.read())
            .field("humidity", self.humidity_sensor.read())
        )

    def stop_sensor(self):
        try:
            self.temperature_sensor.stop()
            self.humidity_sensor.stop()
        except Exception as e:
            print(e)
            pass
