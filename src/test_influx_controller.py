from unittest import TestCase

from influxdb_client import Bucket

from influx_controller import InfluxController
from src.Measurements.measurement_type import MeasurementType


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

    def test_write_measurement(self):
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
                    # write a measurement of that type taking it from a file containing dummy measurements as constants

            #   read the measurement back from influxdb
            #   assert the written and read measurement are the same


        finally:
            influx_controller.delete_bucket(self.TEST_BUCKET_NAME)

