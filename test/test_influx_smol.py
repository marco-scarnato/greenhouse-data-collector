import unittest
from typing import List

from influxdb_client import Bucket, Point

from src.influx_controller import InfluxController
from src.measurements.functions import measurements_to_points
from src.measurements.measurement_type import MeasurementType
from test.resources.dummy_measurements import get_dummy_measurements


class MyTestCase(unittest.TestCase):
    GREENHOUSE_BUCKET_NAME: str = 'greenhouse'

    def test_smol_write_pot(self):
        influx_controller = InfluxController()
        greenhouse_bucket: Bucket = influx_controller.get_bucket(self.GREENHOUSE_BUCKET_NAME)

        dummy_measurements: list = get_dummy_measurements(MeasurementType.POT.get_measurement_name())
        # convert the measurements to points
        dummy_points: List[Point] = measurements_to_points(dummy_measurements)

        # write the dummy measurement to influxdb
        influx_controller.write_points(bucket=greenhouse_bucket, points_list=dummy_points)
        influx_controller.read_all_measurements(bucket=greenhouse_bucket)


if __name__ == '__main__':
    unittest.main()
