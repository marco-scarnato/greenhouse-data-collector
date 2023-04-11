class WaterLevel:
    def __init__(self, adc, channel):
        self.adc = adc
        self.channel = channel

    def read(self):
        # TODO:  convert the value to a number
        return self.adc.read(self.channel)
