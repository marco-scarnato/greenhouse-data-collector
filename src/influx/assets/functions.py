from typing import List

import pytz
from influxdb_client import Point
from src.influx.assets.asset import Asset

from src.influx.assets.greenhouse_asset import GreenhouseAsset
from src.influx.assets.pot_asset import PotAsset
from src.influx.assets.pump_asset import PumpAsset
from src.influx.assets.shelf_asset import ShelfAsset

TIMEZONE = pytz.timezone("Etc/GMT+1")


def measurements_to_points(measurements: list[Asset]) -> List[Point]:
    """
    Converts a list of assets to a list of points
    :param measurements: list of assets
    :return: list of points obtained from the assets
    """
    # points: List[Point] = []
    # for measurement in measurements:
    #     # based on the measurement type, the measurement is converted to a point
    #     if isinstance(measurement, GreenhouseAsset):
    #         points.append(measurement.to_point())
    #     elif isinstance(measurement, ShelfAsset):
    #         points.append(measurement.to_point())
    #     elif isinstance(measurement, PumpAsset):
    #         points.append(measurement.to_point())
    #     elif isinstance(measurement, PotAsset):
    #         points.append(measurement.to_point())
    #     else:
    #         raise ValueError('Invalid measurement type: ' + str(type(measurement)))
    # return points
    # TODO: check
    # why not just:

    return [measurement.to_point() for measurement in measurements]
