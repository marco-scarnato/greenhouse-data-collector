from typing import List
from unittest import TestCase

from influxdb_client import Bucket, Point

from influx_controller import InfluxController
from src.measurements.functions import measurements_to_points
from src.measurements.measurement_type import MeasurementType
from test.resources.dummy_measurements import get_dummy_measurements


# TODO Remove .env from repo

class TestInfluxController(TestCase):
    TEST_BUCKET_NAME: str = 'test'

    def test_create_drop_bucket(self):
        """
        Test the creation and deletion of a database in InfluxDB
        """
        influx_controller = InfluxController()
        influx_controller.create_bucket(self.TEST_BUCKET_NAME)
        assert influx_controller.get_bucket(self.TEST_BUCKET_NAME) is not None
        influx_controller.delete_bucket(self.TEST_BUCKET_NAME)

    def test_write_single_point(self):
        """
        Test the writing of a single point in InfluxDB
        """
        influx_controller = InfluxController()
        influx_controller.create_bucket(self.TEST_BUCKET_NAME)
        test_bucket: Bucket = influx_controller.get_bucket(self.TEST_BUCKET_NAME)
        dummy_point: Point = Point("test").field("test", 1).time(1)
        try:
            influx_controller.write_point(bucket=test_bucket, point=dummy_point)
            read_measurements: list = influx_controller.read_all_measurements(MeasurementType.GREENHOUSE, test_bucket)
            assert len(read_measurements) == 1
            assert dummy_point in read_measurements
        finally:
            influx_controller.delete_bucket(self.TEST_BUCKET_NAME)

    def test_write_measurements(self):
        """
        Test the writing of a measurement in InfluxDB.
        Writes one measurement of each measurement type in influxdb, reads them back and checks if they are the same
        """
        influx_controller = InfluxController()
        influx_controller.create_bucket(self.TEST_BUCKET_NAME)
        test_bucket: Bucket = influx_controller.get_bucket(self.TEST_BUCKET_NAME)

        try:
            # iterate over all measurement types
            for measurement_type in MeasurementType:
                # get a dummy measurement of the current measurement type
                dummy_measurements: list = get_dummy_measurements(measurement_type)
                # convert the measurements to points
                dummy_points: List[Point] = measurements_to_points(dummy_measurements)

                for point in dummy_points:
                    print(point.to_line_protocol())

                # write the dummy measurement to influxdb
                assert influx_controller.write_points(bucket=test_bucket, points_list=dummy_points)
                # read the measurement back from influxdb
                read_measurements: list = influx_controller.read_all_measurements(measurement_type, test_bucket)
                # assert the written and read measurement are the same number
                assert len(dummy_measurements) == len(read_measurements)
                # assert the written and read measurement are the same
                for measurement in dummy_measurements:
                    assert measurement in read_measurements
        finally:
            influx_controller.delete_bucket(self.TEST_BUCKET_NAME)
