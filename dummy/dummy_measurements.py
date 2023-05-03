from datetime import datetime
from typing import List

from influxdb_client import Point
import numpy as np

from src.assets.measurement_type import MeasurementType


start_time = datetime(2023, 4, 11, 12, 0, 0)
end_time = datetime(2023, 4, 11, 13, 0, 0)

time_data = np.linspace(start_time.timestamp(), end_time.timestamp(), 100)
light_data = np.linspace(0, 1, 100)
temp_data = np.linspace(20, 30, 100)
humidity_data = np.linspace(0, 100, 100)
pumpd_water_data = np.linspace(0, 100, 100)
moist_data = np.linspace(0, 100, 100)
health_data = np.linspace(0, 100, 100)
growth_data = np.linspace(0, 100, 100)

np.random.seed(42)
ones_and_twos = np.random.choice([1, 2], size=100, replace=True)
left_and_right = np.random.choice(["left", "right"], size=100, replace=True)

GREENHOUSE_MEASUREMENTS: List[Point] = [
    Point(MeasurementType.GREENHOUSE.get_measurement_name())
    .field("light", light)
    .time(datetime.fromtimestamp(ts))
    for light, ts in zip(light_data, time_data)
]

SHELF_MEASUREMENTS: List[Point] = [
    Point(MeasurementType.SHELF.get_measurement_name())
    .tag("shelf_floor", floor)
    .field("temperature", temp)
    .field("humidity", humidity)
    .time(datetime.fromtimestamp(ts))
    for floor, temp, humidity, ts in zip(
        ones_and_twos, temp_data, humidity_data, time_data
    )
]

PUMP_MEASUREMENTS: List[Point] = [
    Point(MeasurementType.PUMP.get_measurement_name())
    .tag("shelf_floor", shelf)
    .tag("group_position", group)
    .field("pumped_water", water)
    .time(datetime.fromtimestamp(ts))
    for shelf, group, water, ts in zip(
        ones_and_twos, left_and_right, pumpd_water_data, time_data
    )
]

POT_MEASUREMENTS: List[Point] = [
    Point(MeasurementType.POT.get_measurement_name())
    .tag("shelf_floor", shelf)
    .tag("group_position", group)
    .tag("pot_position", pot)
    .tag("plant_id", plant)
    .field("moisture", moist)
    .time(datetime.fromtimestamp(ts))
    for shelf, group, pot, plant, moist, ts in zip(
        ones_and_twos, left_and_right, left_and_right, ones_and_twos, moist_data, time_data
    )
]

PLANT_MEASUREMENTS: List[Point] = [
    Point(MeasurementType.PLANT.get_measurement_name())
    .tag("plant_id", plant)
    .field("health", health)
    .field("growth", growth)
    .time(datetime.fromtimestamp(ts))
    for plant, health, growth, ts in zip(
        ones_and_twos, health_data, growth_data, time_data
    )
]
