import json
import numpy as np

import os

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

        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config.ini"
        )

        # check if the path is to a valid file
        if not os.path.isfile(config_path):
            raise FileNotFoundError("Config file not found")

        conf.read(config_path)

        self.XP = json.loads(conf[sensor + "_values"]["XP"])
        self.FP = np.linspace(range[0], range[1], len(self.XP))

    def interpret(self, value: float) -> float:
        return np.interp(value, self.XP, self.FP)
