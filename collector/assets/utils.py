import datetime
import logging
import os
from typing import List

import pytz
from influxdb_client import Point

from collector.assets.asset import Asset

TIMEZONE = pytz.timezone("Etc/GMT+1")


# FIXME: bit of a useless function, can be removed, decide what to do with TIMEZONE
def assets_to_points(assets: list[Asset]) -> List[Point]:
    """
    Return a list of points containing the measurements for the current state of the assets in input.
    :param assets: list of assets to convert to points
    :return: list of points obtained from the assets
    """
    return [measurement.to_point() for measurement in assets]


def setup_logging(demo: bool = False):
    if demo:
        log_path = "/home/lab/influx_greenhouse/greenhouse-data-collector/demo_log_collector.log"
        first_info_run = "DEMO RUN - DATE: " + str(
            datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        )
    else:
        log_path = (
            "/home/lab/influx_greenhouse/greenhouse-data-collector/log_collector.log"
        )
        first_info_run = "COLLECTOR RUN - DATE: " + str(
            datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        )

    print("COLLECTOR PID: " + str(os.getpid()))
    f = open(log_path, "w")
    f.close()
    logging.basicConfig(filename=log_path, filemode="a", level=logging.NOTSET)
    logging.info(
        "\n\n************************************************************************************"
    )
    logging.info(first_info_run)
    logging.info("COLLECTOR PID: " + str(os.getpid()) + "\n")


def create_stop_script():
    stop_script_path = "/home/lab/stop-collector.sh"
    f = open(stop_script_path, "w")
    f.write("#!/bin/bash\n")
    f.write("kill -SIGINT " + str(os.getpid()) + "\n")
    f.close()
    os.chmod(stop_script_path, 0o777)
