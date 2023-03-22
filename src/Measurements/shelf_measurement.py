from datetime import datetime

from influxdb_client import Point

from src.Measurements.measurement_type import MeasurementType


class ShelfMeasurement:
    """
    Class representing a measurement for the shelf.
    ...
    Attributes
    ----------
    shelf_floor: int
        (tag) floor of the shelf, can be 1 or 2
    temperature: float
        (field) temperature in C° of the shelf at a specific time
    time: datetime
        time of the measurement
    """

    def __init__(self, shelf_floor: int, temperature: float, time: datetime):
        # check if shelf_floor is 1 or 2
        if shelf_floor != 1 and shelf_floor != 2:
            raise ValueError("shelf_floor must be 1 or 2")
        self.shelf_floor = shelf_floor
        self.temperature = temperature
        self.time = time

    def __eq__(self, other):
        return self.shelf_floor == other.shelf_floor \
               and self.temperature == other.temperature \
               and self.time == other.time

    def __str__(self):
        return f'ShelfMeasurement(shelf_floor={self.shelf_floor}, temperature={self.temperature}, time={self.time})'

    def to_point(self) -> Point:
        return Point(MeasurementType.SHELF.get_measurement_name())\
            .tag("shelf_floor", self.shelf_floor)\
            .field("temperature", self.temperature)\
            .time(self.time)

