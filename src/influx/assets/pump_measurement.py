from datetime import datetime

from influxdb_client import Point

from src.influx.assets.measurement_type import MeasurementType


class PumpMeasurement:
    """
    Class representing a measurement for the pump.
    ...
    Attributes
    ----------
    shelf_floor: int
        (tag) floor of the shelf in which the pump is, can be 1 or 2
    group_position: str
        (tag) position of the pot group watered by the pump, can be 'left' or 'right'
    pumped_water: float
        (field) amount of water pumped by the pump in liters
    time: datetime
        time of the measurement
    """

    def __init__(self, shelf_floor: int, group_position: str, pumped_water: float, time: datetime):
        # check if shelf_floor is 1 or 2
        if shelf_floor != 1 and shelf_floor != 2:
            raise ValueError("shelf_floor must be 1 or 2")
        # check if group_position is 'left' or 'right'
        if group_position != 'left' and group_position != 'right':
            raise ValueError("group_position must be 'left' or 'right'")
        self.shelf_floor = shelf_floor
        self.group_position = group_position
        self.pumped_water = pumped_water
        self.time = time

    def __eq__(self, other):
        return self.shelf_floor == other.shelf_floor \
               and self.group_position == other.group_position \
               and self.pumped_water == other.pumped_water \
               and self.time == other.time

    def __str__(self):
        return f'PumpMeasurement(shelf_floor={self.shelf_floor}, group_position={self.group_position}, pumped_water={self.pumped_water}, time={self.time})'

    def to_point(self) -> Point:
        return Point(MeasurementType.PUMP.get_measurement_name())\
            .tag("shelf_floor", self.shelf_floor)\
            .tag("group_position", self.group_position)\
            .field("pumped_water", self.pumped_water)\
            .time(self.time)

    