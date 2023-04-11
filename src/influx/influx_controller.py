import json
from typing import Optional, List, Iterable, Union

from influxdb_client import InfluxDBClient, Bucket, Point
from decouple import config
from influxdb_client.client.flux_table import TableList, FluxStructureEncoder
from influxdb_client.client.write_api import SYNCHRONOUS

from src.influx.assets.measurement_type import MeasurementType


def check_env_variables():
    # check if environment variables are set
    if not config("INFLUX_URL"):
        raise Exception("INFLUX_URL is not set")
    if not config("INFLUX_TOKEN"):
        raise Exception("INFLUX_TOKEN is not set")
    if not config("INFLUX_ORG_ID"):
        raise Exception("INFLUX_ORG_ID is not set")


class InfluxController:
    # https://influxdb-client.readthedocs.io/en/latest/

    def __init__(self):
        """
        Instantiate a new InfluxController object getting the connection parameters
        from the environment variables in .env file
        """
        check_env_variables()
        url, token, org = (
            str(config("INFLUX_URL")),
            str(config("INFLUX_TOKEN")),
            str(config("INFLUX_ORG_ID")),
        )
        self._client: InfluxDBClient = InfluxDBClient(url=url, token=token, org=org)

    def create_bucket(self, bucket_name: str) -> Bucket:
        """
        Create a new bucket in InfluxDB
        :return: new bucket created
        """
        return self._client.buckets_api().create_bucket(bucket_name=bucket_name)

    def delete_bucket(self, bucket_name: str) -> bool:
        """
        Delete a bucket from InfluxDB
        :return: True if deleted, False otherwise
        """

        if (
            self._client.buckets_api().delete_bucket(self.get_bucket(bucket_name))
            is None
        ):
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
        return self._client.write_api(write_options=SYNCHRONOUS).write(
            bucket=bucket.name, org=self._client.org, record=point
        )
