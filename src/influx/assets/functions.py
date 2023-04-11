from typing import List

import pytz
from influxdb_client import Point
from src.influx.assets.asset import Asset


TIMEZONE = pytz.timezone("Etc/GMT+1")


def measurements_to_points(measurements: list[Asset]) -> List[Point]:
    """
    Converts a list of assets to a list of points
    :param measurements: list of assets
    :return: list of points obtained from the assets
    """
    return [measurement.to_point() for measurement in measurements]
