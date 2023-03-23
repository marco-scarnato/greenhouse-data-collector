from datetime import datetime

from influxdb_client import Point

from src.measurements.measurement_type import MeasurementType


class GreenhouseMeasurement:
    """
    Class representing a measurement for the greenhouse.
    ...
    Attributes
    ----------
    light: float
        (field) light level for the greenhouse at a specific time #TODO define format
    time: datetime
        time of the measurement
    """

    def __init__(self, light: float, time: datetime):
        self.light = light
        self.time = time

    def __eq__(self, other):
        return self.light == other.light and self.time == other.time

    def __str__(self):
        return f'GreenhouseMeasurement(light={self.light}, time={self.time})'

    def to_point(self) -> Point:
        return Point(MeasurementType.GREENHOUSE.get_measurement_name())\
            .field("light", self.light)\
            .time(self.time)

