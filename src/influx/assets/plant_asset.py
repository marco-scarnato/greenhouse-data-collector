from dataclasses import dataclass
import time
from datetime import datetime

from influxdb_client import Point

from src.influx.assets.asset import Asset
from src.influx.assets.measurement_type import MeasurementType
from src.influx.influx_controller import InfluxController


@dataclass
class PlantAsset(Asset):
    """
    Class representing a physical plant.

    Attributes
    ----------
    plant_id: str
        (tag) id of the plant
    camera_sensor: any
        camera sensor used to take pictures of the plant and use them to check the plant health and growth. It must
        implement the methods get_plant_health and get_plant_growth
    """
    plant_id: str
    # this is a placeholder for the camera that will be used to take pictures of the plant and use them to check
    # the plant health and growth
    camera_sensor: any

    def to_point(self) -> Point:
        return(
            Point(MeasurementType.PLANT.get_measurement_name())
            .tag("plant_id", self.plant_id)
            .field("health", self.camera_sensor.get_plant_health())
            .field("growth", self.camera_sensor.get_plant_growth())
            .time(datetime.now())
        )

    def read_sensor_data(self, interval: int = 5):
        influx_controller = InfluxController()
        bucket = influx_controller.get_bucket(
            "greenhouse"
        ) or influx_controller.create_bucket("greenhouse")

        while True:
            point = self.to_point()
            influx_controller.write_point(point, bucket)
            time.sleep(interval)

