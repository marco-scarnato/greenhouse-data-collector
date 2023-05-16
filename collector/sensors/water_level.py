from collector.sensors.interpreter import Interpreter
from collector.sensors.mcp3008 import MCP3008


class WaterLevel:
    def __init__(self, adc: MCP3008, channel):
        self.interpreter = Interpreter("water_level").interpret

        self.adc = adc
        self.channel = channel

    def read(self) -> float:
        return self.interpreter(self.adc.read(self.channel))
