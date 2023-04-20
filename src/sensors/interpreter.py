from configparser import ConfigParser
import json
from typing import List
import numpy as np


class Interpreter:
    def __init__(self, sensor: str, range: tuple = (0, 100)):
        conf = ConfigParser()
        conf.read("config.ini")

        self.XP = json.loads(conf[sensor + "_values"]["XP"])
        self.FP = np.linspace(range[0], range[1], len(self.XP))

    def interpret(self, value: float) -> float:
        return np.interp(value, self.XP, self.FP)
