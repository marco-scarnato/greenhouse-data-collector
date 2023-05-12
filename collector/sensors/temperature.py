from typing import Optional

from adafruit_dht import DHT22


class Temperature:
    def __init__(self, temperature_sensor) -> None:
        """Initializes the Temperature sensor. Uses the DHT22 sensor.

        Args:
            temperature_sensor: sensor used to read the temperature.
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
