import datetime
import logging
import os
import time
from typing import List

from influxdb_client import Bucket, Point

from collector.assets import utils
from collector.assets.measurement_type import MeasurementType
from collector.influx.influx_controller import InfluxController


def demo():
    utils.setupLogging(True)

    influx_controller = InfluxController()
    demo_bucket = prepare_demo_bucket(influx_controller)

    pot_measurements: List[Point] = []

    plant_measurement1 = (
        Point(MeasurementType.PLANT.get_measurement_name())
        .tag("plant_id", "1")
        .field("ndvi", 0.3)
    )

    print("Sending demo plant measurements to InfluxDB...")

    influx_controller.write_point(plant_measurement1, demo_bucket)
    print(plant_measurement1.to_line_protocol())
    logging.info(plant_measurement1.to_line_protocol())
    time.sleep(2)

    for moisture_value in range(100, 0, -1):
        pot_measurement = (
            Point(MeasurementType.POT.get_measurement_name())
            .tag("shelf_floor", "1")
            .tag("group_position", "left")
            .tag("pot_position", "left")
            .tag("plant_id", "1")
            .field("moisture", float(moisture_value))
        )
        pot_measurements.append(pot_measurement)

    print("Sending demo pot measurements to InfluxDB...")
    logging.info("Sending demo pot measurements to InfluxDB...")

    for measurement in pot_measurements:
        influx_controller.write_point(measurement, demo_bucket)
        print(measurement.to_line_protocol())
        logging.info(measurement.to_line_protocol())
        time.sleep(1)


def setupLogging():
    log_path = (
        "/home/lab/influx_greenhouse/greenhouse-data-collector/demo_log_collector.log"
    )
    print("COLLECTOR PID: " + str(os.getpid()))
    f = open(log_path, "w")
    f.close()
    logging.basicConfig(filename=log_path, filemode="a", level=logging.NOTSET)
    logging.info(
        "\n\n************************************************************************************"
    )
    logging.info(
        "DEMO RUN - DATE: " + str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    )
    logging.info("COLLECTOR PID: " + str(os.getpid()) + "\n")


def prepare_demo_bucket(influx_controller: InfluxController) -> Bucket:
    influx_controller.delete_bucket("demo")
    return influx_controller.create_bucket("demo")


if __name__ == "__main__":
    """
    Send demo measurements to InfluxDB. Pot measurements are sent in a descending order,
    simulating a plant's moisture decreasing over time.
    """
    demo()
