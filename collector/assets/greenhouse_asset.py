from dataclasses import dataclass
import time
from datetime import datetime

from influxdb_client import Point

from collector.assets.asset import Asset
from collector.influx.influx_controller import InfluxController
from collector.assets.measurement_type import MeasurementType
from collector.sensors.light_level import LightLevel


@dataclass
class GreenhouseAsset(Asset):
    """
    Class representing the Greenhouse asset.

    Attributes:
        light_sensor (LightLevel): sensor used to detect light in the greenhouse
    """

    light_sensor: LightLevel

    def to_point(self) -> Point:
        return (
            Point(MeasurementType.GREENHOUSE.get_measurement_name())
            .field("light", self.light_sensor.read())
        )

    def read_sensor_data(self, interval: int = 5):
        influx_controller = InfluxController()
        bucket = influx_controller.get_bucket("greenhouse")

        while True:
            point = self.to_point()
            print(point)
            influx_controller.write_point(point, bucket)
            time.sleep(interval)
