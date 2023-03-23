from datetime import datetime
from typing import List

from src.measurements.greenhouse_measurement import GreenhouseMeasurement
from src.measurements.pot_measurement import PotMeasurement
from src.measurements.pump_measurement import PumpMeasurement
from src.measurements.shelf_measurement import ShelfMeasurement


class DummyMeasurements:
    GREENHOUSE_MEASUREMENTS: List[GreenhouseMeasurement] = [
        GreenhouseMeasurement(0.5, datetime(2021, 1, 1, 0, 0, 0)),
        GreenhouseMeasurement(0.6, datetime(2021, 1, 1, 0, 1, 0)),
        GreenhouseMeasurement(0.7, datetime(2021, 1, 1, 0, 2, 0)),
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
        PotMeasurement(1, 'left', 'left', 0.5, datetime(2021, 1, 1, 0, 0, 0)),
        PotMeasurement(1, 'left', 'right', 0.6, datetime(2021, 1, 1, 0, 1, 0)),
        PotMeasurement(1, 'right', 'left', 0.7, datetime(2021, 1, 1, 0, 2, 0))
    ]

    def get_dummy_measurements(self, measurement_type: str) -> List:
        if measurement_type == 'greenhouse':
            return self.GREENHOUSE_MEASUREMENTS
        elif measurement_type == 'shelf':
            return self.SHELF_MEASUREMENTS
        elif measurement_type == 'pump':
            return self.PUMP_MEASUREMENTS
        elif measurement_type == 'pot':
            return self.POT_MEASUREMENTS
        else:
            raise ValueError('Invalid measurement type')
