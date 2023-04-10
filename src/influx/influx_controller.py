import json
from typing import Optional, List, Iterable, Union

from influxdb_client import InfluxDBClient, Bucket, Point
from decouple import config
from influxdb_client.client.flux_table import TableList, FluxStructureEncoder
from influxdb_client.client.write_api import SYNCHRONOUS

from src.influx.assets.measurement_type import MeasurementType


def check_env_variables():
    # check if environment variables are set
    if not config('INFLUX_URL'):
        raise Exception('INFLUX_URL is not set')
    if not config('INFLUX_TOKEN'):
        raise Exception('INFLUX_TOKEN is not set')
    if not config('INFLUX_ORG_ID'):
        raise Exception('INFLUX_ORG_ID is not set')


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

    def write_point(self, point: Union[Point, Iterable[Point]], bucket: Bucket) -> bool:
        """
        Write a measurement to bucket
        :param point: measurement to write
        :param bucket: bucket to write to
        """
        return self._client.write_api(write_options=SYNCHRONOUS) \
            .write(bucket=bucket.name, org=self._client.org, record=point)

    def write_points(self, points_list: List[Point], bucket: Bucket) -> bool:
        """
        Write a list of assets to bucket
        :param points_list: list of assets to write
        :param bucket: bucket to write to
        :return: True if written, False otherwise
        """
        # TODO check if records can be written in bulk with a list or a for loop is needed
        for point in points_list:
            self.write_point(point, bucket)

        # return self._client.write_api().write(bucket=bucket.name, record=points_list)
