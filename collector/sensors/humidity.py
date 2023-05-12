from typing import Optional

from adafruit_dht import DHT22


class Humidity:
    def __init__(self, humidity_sensor: DHT22) -> None:
        """Initializes the Humidity sensor. Uses the DHT22 sensor.

        Args:
            pin (Pin): pin connected to the signal line.
            For example for pin GPIO4, board.D4 should be passed as argument.
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
        except Exception as error:
            self.humidity_sensor.exit()
            return None

        return humidity
