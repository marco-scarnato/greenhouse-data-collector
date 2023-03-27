import time
from datetime import datetime

from influxdb_client import Point, Bucket

from src.influx.influx_controller import InfluxController
from src.influx.measurements.measurement_type import MeasurementType
from src.sensors.lightlevel import LightLevel


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

    def __init__(self, light: float, time: datetime, light_sensor: LightLevel):
        self.light = light
        self.time = time
        self.light_sensor = light_sensor

    def __eq__(self, other):
        return self.light == other.light and self.time == other.time

    def __str__(self):
        return f'GreenhouseMeasurement(light={self.light}, time={self.time})'

    def to_point(self) -> Point:
        return Point(MeasurementType.GREENHOUSE.get_measurement_name())\
            .field("light", self.light)\
            .time(self.time)

    def read_sensor_data(self, interval: int = 5):
        influx_controller = InfluxController()
        bucket: Bucket = influx_controller.get_bucket("greenhouse")
        while True:
            self.light = self.light_sensor.read()
            self.time = datetime.now()
            influx_controller.write_point(self.to_point(), bucket)
            time.sleep(interval)
