import threading
import time
from datetime import datetime

from influxdb_client import Point, Bucket

from src.influx.influx_controller import InfluxController
from src.influx.assets.measurement_type import MeasurementType
from src.sensors.humidity import Humidity
from src.sensors.temperature import Temperature


class ShelfMeasurement:
    """
    Class representing a measurement for the shelf.
    ...
    Attributes
    ----------
    shelf_floor: int
        (tag) floor of the shelf, can be 1 or 2
    temperature: float
        (field) temperature in C° of the shelf at a specific time
    humidity: float
        (field) humidity in % of the shelf at a specific time
    time: datetime
        time of the measurement
    """

    def __init__(self,
                 shelf_floor: int,
                 temperature: float,
                 humidity: float,
                 time: datetime,
                 humidity_sensor: Humidity,
                 temperature_sensor: Temperature
                 ):
        # check if shelf_floor is 1 or 2
        if shelf_floor != 1 and shelf_floor != 2:
            raise ValueError("shelf_floor must be 1 or 2")
        self.shelf_floor = shelf_floor

        ########## TODO remove
        self.temperature = temperature
        self.humidity = humidity
        self.time = time
        #############

        self.humidity_sensor = humidity_sensor
        self.temperature_sensor = temperature_sensor

    def __eq__(self, other):
        return self.shelf_floor == other.shelf_floor \
               and self.temperature == other.temperature \
               and self.time == other.time

    def __str__(self):
        return f'ShelfMeasurement(shelf_floor={self.shelf_floor}, temperature={self.temperature}, time={self.time})'

    def to_point(self) -> Point:
        return Point(MeasurementType.SHELF.get_measurement_name()) \
            .tag("shelf_floor", self.shelf_floor) \
            .field("temperature", self.temperature) \
            .field("humidity", self.humidity) \
            .time(self.time)

    def read_sensor_data(self, interval: int = 5):
        influx_controller = InfluxController()
        bucket: Bucket = influx_controller.get_bucket("greenhouse")
        while True:
            self.humidity = self.humidity_sensor.read()
            self.temperature = self.temperature_sensor.read()
            self.time = datetime.now()
            influx_controller.write_point(self.to_point(), bucket)
            print(self.to_point())  # TODO write on db
            time.sleep(interval)
