from typing import Optional

import adafruit_dht


class Temperature:
    def __init__(self, pin) -> None:
        """Initializes the Temperature sensor. Uses the DHT22 sensor.

        Args:
            pin (Pin, optional): pin connected to the signal line.
            For example for pin GPIO4, board.D4 should be passed as argument.
        """
        self.dhtDevice = adafruit_dht.DHT22(pin, use_pulseio=False)

    def read(self) -> Optional[float]:
        temperature_c: Optional[float] = None

        try:
            temperature_c = self.dhtDevice.temperature
        except (
            RuntimeError
        ) as error:  # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            self.dhtDevice.exit()
            return None

        return temperature_c
