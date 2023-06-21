from dataclasses import dataclass

from influxdb_client import Point

from collector.assets.asset import Asset
from collector.assets.measurement_type import MeasurementType
from collector.sensors.moisture import Moisture


@dataclass
class PotAsset(Asset):
    """
    Class representing the Pot asset.

    Attributes:
        shelf_floor (int): floor of the shelf in which the pot is, can be 1 or 2
        group_position (str): position of the pot group in which the pot is placed, can be 'left' or 'right'
        pot_position (str): position of the pot into the pot group, can be 'left' or 'right'
        plant_id (str): id of the plant in the pot
        moisture_sensor (Moisture)
    """

    shelf_floor: str
    group_position: str
    pot_position: str
    plant_id: str
    moisture_sensor: Moisture

    def __post_init__(self):
        if self.shelf_floor != "1" and self.shelf_floor != "2":
            raise ValueError('shelf_floor must be "1" or "2"')

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
            .tag("plant_id", self.plant_id)
            .field("moisture", self.moisture_sensor.read())
        )

    def stop_sensor(self):
        self.moisture_sensor.stop()
