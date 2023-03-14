from unittest import TestCase
from influx_controller import InfluxController


class TestInfluxController(TestCase):
    def test_create_drop_database(self):
        """
        Test the creation and deletion of a database in InfluxDB
        """
        influx_controller = InfluxController()
        influx_controller.create_bucket('test')
        assert influx_controller.get_bucket('test') is not None
        influx_controller.delete_bucket('test')
