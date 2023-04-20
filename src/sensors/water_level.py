from sensors.interpreter import Interpreter


class WaterLevel:
    def __init__(self, adc, channel):
        self.interpreter = Interpreter("water_level")

        self.adc = adc
        self.channel = channel

    def read(self):
        return self.interpreter.interpret(self.adc.read_adc(self.channel))
