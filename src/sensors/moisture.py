class Moisture:
    def __init__(self, adc, channel: int):
        self.adc = adc
        self.channel = channel

    def read(self):
        # TODO: convert the value to a percentage
        return self.adc.read(self.channel)
