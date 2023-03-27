class WaterLevel:

    def __init__(self, adc, channel):
        self.adc = adc
        self.channel = channel

    def read(self):
        # convert the value to a percentage
        return self.adc.read(self.channel)
