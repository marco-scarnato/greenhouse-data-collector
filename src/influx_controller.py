from typing import Optional, List

from influxdb_client import InfluxDBClient, Bucket, Point
from decouple import config

from src.measurements.measurement_type import MeasurementType


def check_env_variables():
    # check if environment variables are set
    if not config('INFLUX_URL'):
        raise Exception('INFLUX_URL is not set')
    if not config('INFLUX_TOKEN'):
        raise Exception('INFLUX_TOKEN is not set')
    if not config('INFLUX_ORG_ID'):
        raise Exception('INFLUX_ORG_ID is not set')

    print("INFLUX_URL: " + config('INFLUX_URL'),
          "\nINFLUX_TOKEN: " + config('INFLUX_TOKEN'),
          "\nINFLUX_ORG_ID: " + config('INFLUX_ORG_ID'))


class InfluxController:
    # https://influxdb-client.readthedocs.io/en/latest/

    def __init__(self):
        """
        Instantiate a new InfluxController object getting the connection parameters
        from the environment variables in .env file
        """
        check_env_variables()
        self._client: InfluxDBClient = InfluxDBClient(url=config('INFLUX_URL'),
                                                      token=config('INFLUX_TOKEN'),
                                                      org=config('INFLUX_ORG_ID'))

        self._client.buckets_api().find_buckets()

    def create_bucket(self, bucket_name: str) -> Optional[Bucket]:
        """
        Create a new bucket in InfluxDB
        :return: new bucket if created, None otherwise
        """
        return self._client.buckets_api().create_bucket(bucket_name=bucket_name)

    def delete_bucket(self, bucket_name: str) -> bool:
        """
        Delete a bucket from InfluxDB
        :return: True if deleted, False otherwise
        """

        if self._client.buckets_api().delete_bucket(self.get_bucket(bucket_name)) is None:
            return False
        else:
            return True

    def get_bucket(self, bucket_name: str) -> Optional[Bucket]:
        """
        Get a bucket from InfluxDB
        :return: bucket if found, None otherwise
        """
        return self._client.buckets_api().find_bucket_by_name(bucket_name)

    def write_measurements(self, measurement_list: List[Point], bucket: Bucket) -> None:
        """
        Write a list of measurements to InfluxDB
        :param measurement_list: list of measurements to write
        :param bucket: bucket to write to
        """
        # TODO check if records can be written in bulk with a list or a for loop is needed
        self._client.write_api().write(bucket=bucket.name, record=measurement_list)

    def read_measurements(self, measurement_type: MeasurementType, bucket: Bucket) -> List[Point]:
        pass
