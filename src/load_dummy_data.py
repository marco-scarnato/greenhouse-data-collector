import unittest


from influx.influx_controller import InfluxController

from test.dummy_measurements import POT_MEASUREMENTS


class MyTestCase(unittest.TestCase):
    GREENHOUSE_BUCKET_NAME: str = "greenhouse_test"

    def test_smol_write_pot(self):
        influx_controller = InfluxController()

        influx_controller.delete_bucket(self.GREENHOUSE_BUCKET_NAME)
        greenhouse_bucket = influx_controller.create_bucket(self.GREENHOUSE_BUCKET_NAME)

        points: list = POT_MEASUREMENTS[:5]

        influx_controller.write_point(bucket=greenhouse_bucket, point=points)


if __name__ == "__main__":
    unittest.main()
