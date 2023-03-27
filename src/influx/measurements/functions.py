from typing import List

import pytz
from influxdb_client import Point

from src.influx.measurements.greenhouse_measurement import GreenhouseMeasurement
from src.influx.measurements.pot_measurement import PotMeasurement
from src.influx.measurements.pump_measurement import PumpMeasurement
from src.influx.measurements.shelf_measurement import ShelfMeasurement

TIMEZONE = pytz.timezone('Etc/GMT+1')


def measurements_to_points(measurements: list) -> List[Point]:
    """
    Converts a list of measurements to a list of points
    :param measurements: list of measurements
    :return: list of points obtained from the measurements
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
