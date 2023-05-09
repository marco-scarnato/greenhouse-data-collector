from dataclasses import dataclass
import time
from datetime import datetime

from influxdb_client import Point

from assets.asset import Asset
from assets.measurement_type import MeasurementType
from influx.influx_controller import InfluxController

from sensors.ndvi import NDVI

# TODO ask Eduard, do imports make sense?


@dataclass
class PlantAsset(Asset):
    """
    Class representing the Plant asset.

    Attributes
    ----------
    plant_id: str
        (tag) id of the plant
    infrared_camera: NDVI
        infrared camera used to take pictures of the plant and calculate its health (expressed as NDVI)
    """
    plant_id: str
    infrared_camera: NDVI

    def to_point(self) -> Point:
        return(
            Point(MeasurementType.PLANT.get_measurement_name())
            .tag("plant_id", self.plant_id)
            .field("ndvi", self.infrared_camera.read())
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

