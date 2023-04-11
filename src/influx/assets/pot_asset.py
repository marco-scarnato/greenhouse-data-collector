from dataclasses import dataclass
import time
from datetime import datetime

from influxdb_client import Point
from src.influx.assets.asset import Asset

from src.influx.influx_controller import InfluxController
from src.influx.assets.measurement_type import MeasurementType
from src.sensors.moisture import Moisture


@dataclass
class PotAsset(Asset):
    """
    Class representing a measurement for the shelf.
    ...
    Attributes
    ----------
    shelf_floor: int
        (tag) floor of the shelf in which the pot is, can be 1 or 2
    group_position: str
        (tag) position of the pot group in which the pot is placed, can be 'left' or 'right'
    pot_position: str
        (tag) position of the pot into the pot group, can be 'left' or 'right'
    moisture_sensor: Moisture
        moisture sensor of the pot
    """

    shelf_floor: int
    group_position: str
    pot_position: str
    moisture_sensor: Moisture

    def __post_init__(self):
        if self.shelf_floor != 1 and self.shelf_floor != 2:
            raise ValueError("shelf_floor must be 1 or 2")

        if self.group_position != "left" and self.group_position != "right":
            raise ValueError("group_position must be 'left' or 'right'")

        if self.pot_position != "left" and self.pot_position != "right":
            raise ValueError("pot_position must be 'left' or 'right'")

    def to_point(self) -> Point:
        return (
            Point(MeasurementType.POT.get_measurement_name())
            .tag("shelf_floor", self.shelf_floor)
            .tag("group_position", self.group_position)
            .tag("pot_position", self.pot_position)
            .field("moisture", self.moisture_sensor.read())
            .time(datetime.now())
        )

    def read_sensor_data(self, interval: int = 5):
        influx_controller = InfluxController()
        bucket = influx_controller.get_bucket(
            "greenhouse"
        ) or influx_controller.create_bucket("greenhouse")

        while True:
            influx_controller.write_point(self.to_point(), bucket)
            time.sleep(interval)
