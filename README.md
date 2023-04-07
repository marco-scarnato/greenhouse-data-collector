## Sirius Greenhouse - InfluxDB client

This is a client library for InfluxDB. It is used to send data obtained from the sensors of a greenhouse to a Database in InfluxDB.

The script should run on a Raspberry Pi, which is connected to the sensors and the InfluxDB server.

The sensors retrieve data related to:
 - Light intensity of the greenhouse (in lux)
 - Temperature of a shelf in the greenhouse (in °C)
 - Moisture level of a pot in the greenhouse (in %)
 - Quantity of water pumped from the water tanks (in liters)

### Installation

### Testing

To load dummy data on your local influxdb database, run the following command from the root of the project:

```bash
python src/load_dummy_data.py
```

