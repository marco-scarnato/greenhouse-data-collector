from unittest import TestCase

from influxdb_client import Bucket

from influx_controller import InfluxController
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
                # write the dummy measurement to influxdb
                influx_controller.write_measurements(dummy_measurements, test_bucket)
                # read the measurement back from influxdb
                read_measurements = influx_controller.read_measurements(measurement_type, test_bucket)
                # assert the written and read measurement are the same
                for measurement in dummy_measurements:
                    assert measurement in read_measurements
        finally:
            influx_controller.delete_bucket(self.TEST_BUCKET_NAME)
