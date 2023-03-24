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


def query_result_to_points(result):
    """
    Convert a query result to a list of points
    :param result: query result
    :return: list of points
    """
    points: List[Point] = []
    # convert result to list of points
    for table in result:
        for record in table.records:
            point: Point = Point("measurement_name").time(record.get_time())
            for key, value in record.values.items():
                # skip private fields
                if key.startswith('_'):
                    continue
                if key in table.columns:
                    point.field(key, value)
                else:
                    point.tag(key, value)
            points.append(point)
    return points


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

    def write_point(self, point: Point, bucket: Bucket) -> None:
        """
        Write a measurement to bucket
        :param point: measurement to write
        :param bucket: bucket to write to
        """
        self._client.write_api().write(bucket=bucket.name, record=point)

    def write_points(self, points_list: List[Point], bucket: Bucket) -> bool:
        """
        Write a list of measurements to bucket
        :param points_list: list of measurements to write
        :param bucket: bucket to write to
        :return: True if written, False otherwise
        """
        # TODO check if records can be written in bulk with a list or a for loop is needed
        return self._client.write_api().write(bucket=bucket.name, record=points_list, org=config('INFLUX_ORG_ID'))

    def read_all_measurements(self, measurement_type: Optional[MeasurementType], bucket: Bucket) -> List[Point]:
        """
        Read all measurements from bucket, if measurement_type is specified only measurements of that type are returned.
        Otherwise, all measurements are returned
        :param measurement_type: type of measurement to read
        :param bucket: bucket to read from
        :return: list of measurements read from bucket
        """
        if measurement_type is None:
            query = f'from(bucket: "{bucket.name}") |> range(start: 0)'
        else:
            query = f'from(bucket: "{bucket.name}") |> range(start: 0) |> ' \
                    f'filter(fn: (r) => r._measurement == "{measurement_type.value}") '

        result = self._client.query_api().query(query)
        points = query_result_to_points(result)

        return points

