import time
from abc import ABC, abstractmethod

from influxdb_client import Point

from collector.influx.influx_controller import InfluxController


class Asset(ABC):
    """
    Abstract class for an asset.
    """
    influx_controller: InfluxController = InfluxController()
    sensor_read_interval: int = 5

    def set_sensor_read_interval(self, sensor_read_interval: int) -> None:
        """
        Set the sensor read interval.
        :param sensor_read_interval: sensor read interval in seconds
        """
        self.sensor_read_interval = sensor_read_interval

    @abstractmethod
    def to_point(self) -> Point:
        """
        Convert the asset to a point.
        Returns a point with the fields and tags of the asset.
        :return: Point
        """
        pass

    def read_sensor_data(self) -> None:
        """
        Read the sensor data and write a point to influxdb. The point is created by the to_point() method.
        Repeat every sensor_read_interval seconds.
        """
        bucket = self.influx_controller.get_bucket("greenhouse")

        while True:
            point = self.to_point()
            print(point)
            self.influx_controller.write_point(point, bucket)
            time.sleep(self.sensor_read_interval)
