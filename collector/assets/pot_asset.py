from dataclasses import dataclass
import time
from datetime import datetime
from typing import Dict

from influxdb_client import Point
from collector.assets.asset import Asset

from collector.influx.influx_controller import InfluxController
from collector.assets.measurement_type import MeasurementType
from collector.sensors.moisture import Moisture


@dataclass
class PotAsset(Asset):
    """
    Class representing the Pot asset.

    Attributes
    ----------
    shelf_floor: int
        (tag) floor of the shelf in which the pot is, can be 1 or 2
    group_position: str
        (tag) position of the pot group in which the pot is placed, can be 'left' or 'right'
    pot_position: str
        (tag) position of the pot into the pot group, can be 'left' or 'right'
    plant_id: str
        (tag) id of the plant in the pot
    moisture_sensor: Moisture
        moisture sensor of the pot
    """

    shelf_floor: int
    group_position: str
    pot_position: str
    plant_id: str
    moisture_sensor: Moisture

    def __post_init__(self):
        if self.shelf_floor != 1 and self.shelf_floor != 2:
            raise ValueError("shelf_floor must be 1 or 2")

        if self.group_position != "left" and self.group_position != "right":
            raise ValueError("group_position must be 'left' or 'right'")

        if self.pot_position != "left" and self.pot_position != "right":
            raise ValueError("pot_position must be 'left' or 'right'")

    def __init__(self, pot_dict: Dict, mcp3008):
        self.shelf_floor = pot_dict['shelf_floor']
        self.group_position = pot_dict['group_position']
        self.pot_position = pot_dict['pot_position']
        self.moisture_sensor = Moisture(mcp3008, pot_dict['moisture_adc_channel'])
        self.plant_id = pot_dict['plant_id']
        self.influx_controller = InfluxController()

    def to_point(self) -> Point:
        return (
            Point(MeasurementType.POT.get_measurement_name())
            .tag("shelf_floor", self.shelf_floor)
            .tag("group_position", self.group_position)
            .tag("pot_position", self.pot_position)
            .tag("plant_id", self.plant_id)
            .field("moisture", self.moisture_sensor.read())
        )

    def read_sensor_data(self, interval: int = 5):
        bucket = self.influx_controller.get_bucket("greenhouse")

        while True:
            point = self.to_point()
            print(point)
            self.influx_controller.write_point(point, bucket)
            time.sleep(interval)
