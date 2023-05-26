import time
from typing import List

from influxdb_client import Point

from collector.assets.measurement_type import MeasurementType
from collector.influx.influx_controller import InfluxController


def demo():
    influx_controller = InfluxController()
    demo_bucket = influx_controller.create_bucket_if_not_exists("demo")

    pot_measurements: List[Point] = []

    for moisture_value in range(100, 0, -1):
        pot_measurement = Point(MeasurementType.POT.get_measurement_name()) \
            .tag("shelf_floor", "1").tag("group_position", "left").tag("pot_position", "left").tag("plant_id", "1") \
            .field("moisture", float(moisture_value))
        pot_measurements.append(pot_measurement)

    for measurement in pot_measurements:
        influx_controller.write_point(measurement, demo_bucket)
        print(measurement.to_line_protocol())
        time.sleep(1)


if __name__ == "__main__":
    """
    Send demo measurements to InfluxDB. Pot measurements are sent in a descending order, simulating a 
    plant's moisture decreasing over time.
    """
    demo()
