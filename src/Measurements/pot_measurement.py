from datetime import datetime

from influxdb_client import Point

from src.Measurements.measurement_type import MeasurementType


class PotMeasurement:
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
    moisture: float
        (field) moisture level of the pot at a specific time
    time: datetime
        time of the measurement
    """

    def __init__(self, shelf_floor: int, group_position: str, pot_position: str, moisture: float, time: datetime):
        # check if shelf_floor is 1 or 2
        if shelf_floor != 1 and shelf_floor != 2:
            raise ValueError("shelf_floor must be 1 or 2")
        # check if group_position is 'left' or 'right'
        if group_position != 'left' and group_position != 'right':
            raise ValueError("group_position must be 'left' or 'right'")
        # check if pot_position is 'left' or 'right'
        if pot_position != 'left' and pot_position != 'right':
            raise ValueError("pot_position must be 'left' or 'right'")
        self.shelf_floor = shelf_floor
        self.group_position = group_position
        self.pot_position = pot_position
        self.moisture = moisture
        self.time = time

    def __eq__(self, other):
        return self.shelf_floor == other.shelf_floor \
               and self.group_position == other.group_position \
               and self.pot_position == other.pot_position \
               and self.moisture == other.moisture \
               and self.time == other.time

    def __str__(self):
        return f'ShelfMeasurement(shelf_floor={self.shelf_floor}, group_position={self.group_position}, pot_position={self.pot_position}, moisture={self.moisture}, time={self.time})'

    def to_point(self) -> Point:
        return Point(MeasurementType.SHELF.get_measurement_name())\
            .tag("shelf_floor", self.shelf_floor)\
            .tag("group_position", self.group_position)\
            .tag("pot_position", self.pot_position)\
            .field("moisture", self.moisture)\
            .time(self.time)

