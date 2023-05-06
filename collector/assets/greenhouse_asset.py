from dataclasses import dataclass
import time
from datetime import datetime

from influxdb_client import Point

from assets.asset import Asset
from influx.influx_controller import InfluxController
from assets.measurement_type import MeasurementType
from sensors.light_level import LightLevel


@dataclass
class GreenhouseAsset(Asset):
    """
    Class representing the Greenhouse asset.

    Attributes
    ----------
    light_sensor: LightLevel
        sensor used to detect light in the greenhouse
    """

    light_sensor: LightLevel

    def to_point(self) -> Point:
        return (
            Point(MeasurementType.GREENHOUSE.get_measurement_name())
            .field("light", self.light_sensor.read())
            .time(datetime.now())
        )

    def read_sensor_data(self, interval: int = 5):
        influx_controller = InfluxController()
        bucket = influx_controller.get_bucket(
            "greenhouse"
        ) or influx_controller.create_bucket("greenhouse")

        while True:
            influx_controller.write_point(self.to_point(), bucket)
            time.sleep(interval)
