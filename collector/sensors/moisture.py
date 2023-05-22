from collector.sensors.interpreter import Interpreter
from collector.sensors.mcp3008 import MCP3008


class Moisture:
    def __init__(self, adc: MCP3008, channel: int) -> None:
        """Initializes the Moisture sensor.

        Args:
            adc (MCP3008): the analog to digital converter
            channel (int): the channel of the ADC to which the sensor is connected
        """
        self.interpret = Interpreter("moisture").interpret

        self.adc = adc
        self.channel = channel

    def read(self) -> float:
        return self.interpret(self.adc.read(self.channel))
