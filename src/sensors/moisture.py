from sensors.interpreter import Interpreter
from sensors.mcp3008 import MCP3008


class Moisture:
    def __init__(self, adc : MCP3008, channel: int) -> None:
        self.interpret = Interpreter("moisture").interpret

        self.adc = adc
        self.channel = channel

    def read(self) -> float:
        return self.interpret(self.adc.read(self.channel))
