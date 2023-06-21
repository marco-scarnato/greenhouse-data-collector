from typing import Optional

from adafruit_dht import DHT22


class Humidity:
    def __init__(self, humidity_sensor: DHT22) -> None:
        """Initializes the Humidity sensor. Uses the DHT22 sensor.

        Args:
            humidity_sensor: sensor used to read the humidity.
        """
        self.humidity_sensor = humidity_sensor

    def read(self) -> Optional[float]:
        humidity: Optional[float] = None

        try:
            humidity = self.humidity_sensor.humidity
        except (
            RuntimeError
        ) as error:  # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception:
            self.humidity_sensor.exit()
            return None

        return humidity

    def stop(self):
        self.humidity_sensor.exit()
