from typing import Optional

import board
import adafruit_dht


class Temperature:

    def __init__(self, pin=board.D4):
        self.dhtDevice = adafruit_dht.DHT22(pin)

    def read(self):
        temperature_c: Optional[float] = None

        try:
            temperature_c = self.dhtDevice.temperature
        except RuntimeError as error:  # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            self.dhtDevice.exit()
            return None

        return temperature_c
