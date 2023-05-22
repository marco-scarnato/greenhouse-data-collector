import unittest
from datetime import datetime
from unittest import TestCase

from influxdb_client import Point

from influx.influx_controller import InfluxController
from assets.assets_utils import TIMEZONE
from dummy_measurements import GREENHOUSE_MEASUREMENTS


class TestInfluxController(TestCase):
    TEST_BUCKET_NAME: str = "dummy"

    def test_create_drop_bucket(self):
        """
        Test the creation and deletion of a database in InfluxDB
        """
        influx_controller = InfluxController()
        influx_controller.create_bucket(self.TEST_BUCKET_NAME)
        assert influx_controller.get_bucket(self.TEST_BUCKET_NAME) is not None
        influx_controller.delete_bucket(self.TEST_BUCKET_NAME)

    def test_write_1_point(self):
        """
        Test the writing of a single point in InfluxDB
        """
        influx_controller = InfluxController()
        test_bucket = influx_controller.create_bucket(self.TEST_BUCKET_NAME)
        dummy_point: Point = (
            Point("name_test")
            .field("field_test", 1)
            .tag("tag_test", 2)
            .time(datetime.now(tz=TIMEZONE))
        )
        try:
            influx_controller.write_point(bucket=test_bucket, point=dummy_point)
        finally:
            influx_controller.delete_bucket(self.TEST_BUCKET_NAME)

    def test_write_multiple_points(self):
        """
        Test the writing of multiple points in InfluxDB
        """
        influx_controller = InfluxController()
        bucket_name = self.TEST_BUCKET_NAME

        try:
            test_bucket = influx_controller.create_bucket(bucket_name)
            point = GREENHOUSE_MEASUREMENTS[3]

            assert influx_controller.write_point(bucket=test_bucket, point=point)
        finally:
            influx_controller.delete_bucket(bucket_name)


if __name__ == "__main__":
    unittest.main()
