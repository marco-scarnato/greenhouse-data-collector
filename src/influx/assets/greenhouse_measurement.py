import time
from datetime import datetime

from influxdb_client import Point, Bucket

from src.influx.assets.asset import Asset
from src.influx.influx_controller import InfluxController
from src.influx.assets.measurement_type import MeasurementType
from src.sensors.lightlevel import LightLevel


class Greenhouse(Asset):
    """
    Class representing the greenhouse asset.
    ...
    Attributes
    ----------
    light: float
        (field) most recent light detection for the greenhouse #TODO define format
    time: datetime
        time of the most recent detection for the greenhouse
    light_sensor: LightLevel
        sensor used to detect light in the greenhouse
    """

    def __init__(self, light_sensor: LightLevel):
        self.light = None
        self.time = None
        self.light_sensor = light_sensor

    def __eq__(self, other):
        return self.light == other.light and self.time == other.time

    def __str__(self):
        return f'GreenhouseMeasurement(light={self.light}, time={self.time})'

    def to_point(self) -> Point:
        """
        Get a point measurement for the greenhouse.
        It contains the light level and timestamp of the last sensor detection.
        :return: Point(light, time)
        """
        return Point(MeasurementType.GREENHOUSE.get_measurement_name())\
            .field("light", self.light)\
            .time(self.time)

    def read_sensor_data(self, interval: int = 5):
        """
        Read the sensor data and write it to the database.
        :param interval: interval in seconds between each light sensor reading
        """
        influx_controller = InfluxController()
        bucket: Bucket = influx_controller.get_bucket("greenhouse")
        while True:
            # update light level of the greenhouse measurements
            self.light = self.light_sensor.read()
            # update time of the greenhouse measurements
            self.time = datetime.now()
            # write the point to influxdb
            influx_controller.write_point(self.to_point(), bucket)
            time.sleep(interval)
