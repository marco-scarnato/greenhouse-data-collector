from typing import Optional

from adafruit_dht import DHT22


class Temperature:
    def __init__(self, temperature_sensor: DHT22) -> None:
        """Initializes the Temperature sensor. Uses the DHT22 sensor.

        Args:
            pin (Pin, optional): pin connected to the signal line.
            For example for pin GPIO4, board.D4 should be passed as argument.
        """
        self.temperature_sensor = temperature_sensor

    def read(self) -> Optional[float]:
        temperature_c: Optional[float] = None

        try:
            temperature_c = self.temperature_sensor.temperature
        except (
            RuntimeError
        ) as error:  # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            self.temperature_sensor.exit()
            return None

        return temperature_c
