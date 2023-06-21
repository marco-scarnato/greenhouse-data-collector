import logging
import sys
import threading
import time
from abc import ABC, abstractmethod

from influxdb_client import Point

from collector.influx.influx_controller import InfluxController


class Asset(ABC):
    """
    Abstract class for an asset.
    """

    stop_flag: threading.Event = threading.Event()
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

    @abstractmethod
    def stop_sensor(self):
        pass

    def read_sensor_data(self) -> None:
        """
        Read the sensor data and write a point to influxdb. The point is created by the to_point() method.
        Repeat every sensor_read_interval seconds.
        """
        print("Reading sensor data...")
        try:
            bucket = self.influx_controller.get_bucket("greenhouse")
            while not self.stop_flag.is_set():
                point = self.to_point()
                print(point)
                logging.info(point)
                if not self.influx_controller.write_point(point, bucket):
                    # if write fails, try again every 5 seconds
                    bucket = None
                    while bucket is None:
                        print("Bucket not found, trying again in 5 seconds...")
                        logging.warning(
                            "Bucket not found, trying again in 5 seconds..."
                        )
                        time.sleep(5)
                        bucket = self.influx_controller.get_bucket("greenhouse")
                time.sleep(self.sensor_read_interval)
        except Exception as e:
            # TODO add stacktrace
            print("Error while reading sensor data: " + str(e))
            logging.error("Error while reading sensor data: " + str(e))
            self.stop_sensor()
            sys.exit(1)

        self.stop_sensor()
        sys.exit(0)

    def stop_thread(self):
        """
        Stop the thread.
        """
        self.stop_flag.set()
