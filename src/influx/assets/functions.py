from typing import List

import pytz
from influxdb_client import Point

from src.influx.assets.greenhouse_measurement import GreenhouseMeasurement
from src.influx.assets.pot_measurement import PotMeasurement
from src.influx.assets.pump_measurement import PumpMeasurement
from src.influx.assets.shelf_measurement import ShelfMeasurement

TIMEZONE = pytz.timezone('Etc/GMT+1')


def measurements_to_points(measurements: list) -> List[Point]:
    """
    Converts a list of assets to a list of points
    :param measurements: list of assets
    :return: list of points obtained from the assets
    """
    points: List[Point] = []
    for measurement in measurements:
        # based on the measurement type, the measurement is converted to a point
        if isinstance(measurement, GreenhouseMeasurement):
            points.append(measurement.to_point())
        elif isinstance(measurement, ShelfMeasurement):
            points.append(measurement.to_point())
        elif isinstance(measurement, PumpMeasurement):
            points.append(measurement.to_point())
        elif isinstance(measurement, PotMeasurement):
            points.append(measurement.to_point())
        else:
            raise ValueError('Invalid measurement type: ' + str(type(measurement)))
    return points
