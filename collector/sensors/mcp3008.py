from spidev import SpiDev


class MCP3008:
    """
    Analog to digital converter for the Raspberry Pi.
    Uses the SPI protocol to communicate with the Raspberry Pi.
    """

    def __init__(self, bus=0, device=0) -> None:
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000  # 1MHz

    def read(self, channel=0) -> float:
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data / 1023.0 * 3.3

    def close(self):
        self.spi.close()
