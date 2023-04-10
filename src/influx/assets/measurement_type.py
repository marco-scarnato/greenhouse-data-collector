from enum import Enum


class MeasurementType(Enum):
    """
    Enum containing measurement types: greenhouse, shelf, pump, pot
    """
    GREENHOUSE = 'greenhouse'
    SHELF = 'shelf'
    PUMP = 'pump'
    POT = 'pot'

    """
    Returns the measurement name for a given measurement type. It adds the prefix "ast:" to the measurement type
    """
    def get_measurement_name(self):
        return 'ast:' + self.value
