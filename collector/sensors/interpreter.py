import json
import numpy as np

from collector.config import CONFIG_PATH

try:
    # >3.2
    from configparser import ConfigParser
except ImportError:
    # python27
    # Refer to the older SafeConfigParser as ConfigParser
    from configparser import SafeConfigParser as ConfigParser


class Interpreter:
    """
    Class that interprets raw values from sensors to meaningful values.
    Uses a linear interpolation, a variable number of points can be used
    to define the interpolation function.
    """

    def __init__(self, sensor: str, range: tuple = (0, 100)):
        conf = ConfigParser()
        conf.read(CONFIG_PATH)

        self.XP = json.loads(conf[sensor + "_values"]["XP"])
        self.FP = np.linspace(range[0], range[1], len(self.XP))

        # If the first value is greater than the last one, reverse the arrays
        # numpy.interp does not work with decreasing arrays
        if self.XP[0] > self.XP[-1]:
            self.XP = self.XP[::-1]
            self.FP = self.FP[::-1]

    def interpret(self, value: float) -> float:
        return np.interp(value, self.XP, self.FP)
