from abc import ABC, abstractmethod

from influxdb_client import Point


class Asset(ABC):
    """
    Abstract class for an asset.
    """

    @abstractmethod
    def to_point(self) -> Point:
        """
        Convert the asset to a point.
        Returns a point with the fields and tags of the asset.
        :return: Point
        """
        pass

    @abstractmethod
    def read_sensor_data(self, interval: int) -> None:
        """
        Read the sensor data and write a point to influxdb. The point is created by the to_point() method.
        :param interval: interval in seconds between each sensor reading
        """
        pass

