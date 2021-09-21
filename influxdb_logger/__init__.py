__version__ = "0.1.0"

import logging

from influxdb_client import InfluxDBClient
from influxdb_client.domain.buckets import Buckets
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxHandler(logging.Handler):

    tag_key: str
    tag_value: str

    default_format = (
        "logger,{tag_key}={tag_value},{field_key}={field_value},{timestamp}"
    )

    def __init__(
        self,
        url: str,
        token: str,
        bucket_name: str,
        org: str,
        tag_key: str = None,
        tag_value: str = None,
    ) -> None:
        """Creates the InfluxDB Handler Object.
        Will not take any formatter
        """
        super().__init__()
        self.url = url
        self.token = token
        self.bucket_name = bucket_name
        self.org = org
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.buckets_api = self.client.buckets_api()
        self._check_token()

        # Checking for tags
        if tag_key and tag_value:
            super().setFormatter(
                logging.Formatter(
                    f'logger,{tag_key}={tag_value} %(levelname)s="Line: %(lineno)d Message: %(message)s"'
                )
            )
        else:
            super().setFormatter(
                logging.Formatter(f'logger %(levelname)s="%(lineno)d %(message)s"')
            )

    def _check_token(self) -> None:
        """Checks if the entered credential works and bucket exist"""
        bucket_list: Buckets = self.buckets_api.find_buckets()

        # TO DO - Check if bucket name is there in bucket_list

    def emit(self, record) -> None:
        log = self.format(record)
        print(f"Emitting: {log}")
        self.write_api.write(bucket=self.bucket_name, org=self.org, record=log)
