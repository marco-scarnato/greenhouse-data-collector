from datetime import datetime
from typing import List

from src.measurements.functions import TIMEZONE
from src.measurements.greenhouse_measurement import GreenhouseMeasurement
from src.measurements.measurement_type import MeasurementType
from src.measurements.pot_measurement import PotMeasurement
from src.measurements.pump_measurement import PumpMeasurement
from src.measurements.shelf_measurement import ShelfMeasurement


class DummyMeasurements:
    """
    Class containing dummy measurements for testing purposes
    """
    GREENHOUSE_MEASUREMENTS: List[GreenhouseMeasurement] = [
        GreenhouseMeasurement(0.5, datetime.now(tz=TIMEZONE)),
        GreenhouseMeasurement(0.6, datetime.now(tz=TIMEZONE)),
        GreenhouseMeasurement(0.7, datetime.now(tz=TIMEZONE)),
    ]

    SHELF_MEASUREMENTS: List[ShelfMeasurement] = [
        ShelfMeasurement(1, 0.5, datetime(2021, 1, 1, 0, 0, 0)),
        ShelfMeasurement(1, 0.6, datetime(2021, 1, 1, 0, 1, 0)),
        ShelfMeasurement(2, 0.7, datetime(2021, 1, 1, 0, 2, 0))
    ]

    PUMP_MEASUREMENTS: List[PumpMeasurement] = [
        PumpMeasurement(1, 'left', 0.5, datetime(2021, 1, 1, 0, 0, 0)),
        PumpMeasurement(1, 'left', 0.6, datetime(2021, 1, 1, 0, 1, 0)),
        PumpMeasurement(1, 'right', 0.7, datetime(2021, 1, 1, 0, 2, 0))
    ]

    POT_MEASUREMENTS: List[PotMeasurement] = [
        PotMeasurement(1, 'right', 'left', 15, datetime(2023, 3, 26, 0, 0, 0)),
        PotMeasurement(1, 'right', 'left', 10, datetime(2023, 3, 25, 0, 1, 0)),
        PotMeasurement(1, 'right', 'left', 3, datetime(2023, 3, 24, 0, 2, 0))
    ]


def get_dummy_measurements(measurement_type: MeasurementType) -> List:
    if measurement_type == MeasurementType.GREENHOUSE:
        return DummyMeasurements.GREENHOUSE_MEASUREMENTS
    elif measurement_type == MeasurementType.SHELF:
        return DummyMeasurements.SHELF_MEASUREMENTS
    elif measurement_type == MeasurementType.PUMP:
        return DummyMeasurements.PUMP_MEASUREMENTS
    elif measurement_type == MeasurementType.POT:
        return DummyMeasurements.POT_MEASUREMENTS
    else:
        raise ValueError('Invalid measurement type')
