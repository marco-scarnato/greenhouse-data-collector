from typing import List

import pytz
from influxdb_client import Point
from src.influx.assets.asset import Asset


TIMEZONE = pytz.timezone("Etc/GMT+1")


def assets_to_points(assets: list[Asset]) -> List[Point]:
    """
    Return a list of points containing the measurements for the current state of the assets in input.
    :param assets: list of assets to convert to points
    :return: list of points obtained from the assets
    """
    return [measurement.to_point() for measurement in assets]
