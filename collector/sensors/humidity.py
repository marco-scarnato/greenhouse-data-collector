from typing import Optional

import adafruit_dht


class Humidity:
    def __init__(self, pin) -> None:
        """Initializes the Humidity sensor. Uses the DHT22 sensor.

        Args:
            pin (Pin): pin connected to the signal line.
            For example for pin GPIO4, board.D4 should be passed as argument.
        """
        self.dhtDevice = adafruit_dht.DHT22(pin, use_pulseio=False)

    def read(self) -> Optional[float]:
        humidity: Optional[float] = None

        try:
            humidity = self.dhtDevice.humidity
        except (
                RuntimeError
        ) as error:  # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            self.dhtDevice.exit()
            return None

        return humidity
