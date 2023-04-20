from sensors.interpreter import Interpreter


class Moisture:
    def __init__(self, adc, channel: int):
        self.interpreter = Interpreter("moisture")

        self.adc = adc
        self.channel = channel

    def read(self):
        return self.interpreter.interpret(self.adc.read_adc(self.channel))
