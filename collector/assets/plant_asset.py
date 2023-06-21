from dataclasses import dataclass

from influxdb_client import Point

from collector.assets.asset import Asset
from collector.assets.measurement_type import MeasurementType
from collector.sensors.ndvi import NDVI


@dataclass
class PlantAsset(Asset):
    """
    Class representing the Plant asset.

    Attributes:
        plant_id (str): id of the plant
        infrared_camera (NDVI): infrared camera used to take pictures of the plant and calculate its health (expressed as NDVI)
    """

    plant_id: str
    infrared_camera: NDVI

    def to_point(self) -> Point:
        return (
            Point(MeasurementType.PLANT.get_measurement_name())
            .tag("plant_id", self.plant_id)
            .field("ndvi", self.infrared_camera.read())
        )

    def stop_sensor(self):
        try:
            self.infrared_camera.stop()
        except Exception as e:
            print(e)
            pass
