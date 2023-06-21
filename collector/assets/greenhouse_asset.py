from dataclasses import dataclass

from influxdb_client import Point

from collector.assets.asset import Asset
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
        return Point(MeasurementType.GREENHOUSE.get_measurement_name()).field(
            "light", self.light_sensor.read()
        )

    def stop_sensor(self):
        self.light_sensor.stop()
