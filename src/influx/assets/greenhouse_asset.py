from dataclasses import dataclass
import time
from datetime import datetime

from influxdb_client import Point

from src.influx.assets.asset import Asset
from src.influx.influx_controller import InfluxController
from src.influx.assets.measurement_type import MeasurementType
from src.sensors.lightlevel import LightLevel


@dataclass
class GreenhouseAsset(Asset):
    """
    Class representing the greenhouse asset.
    ...
    Attributes
    ----------
    light_sensor: LightLevel
        sensor used to detect light in the greenhouse
    """

    light_sensor: LightLevel

    def to_point(self) -> Point:
        """
        Get a point measurement for the greenhouse.
        It contains the light level and timestamp of the last sensor detection.
        :return: Point(light, time)
        """
        return (
            Point(MeasurementType.GREENHOUSE.get_measurement_name())
            .field("light", self.light_sensor.read())
            .time(datetime.now())
        )

    def read_sensor_data(self, interval: int = 5):
        """
        Read the sensor data and write it to the database.
        :param interval: interval in seconds between each light sensor reading
        """
        influx_controller = InfluxController()
        bucket = influx_controller.get_bucket(
            "greenhouse"
        ) or influx_controller.create_bucket("greenhouse")

        while True:
            influx_controller.write_point(self.to_point(), bucket)
            time.sleep(interval)
