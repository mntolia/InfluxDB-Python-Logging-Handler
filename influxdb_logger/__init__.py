__version__ = '0.1.0'

import logging

import httpx


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
        level=logging.INFO,
    ) -> None:
        """Creates the InfluxDB Handler Object.
        Will not take any formatter
        """
        super().__init__(level=level)
        self.url = url
        self.token = token
        self.bucket_name = bucket_name
        self.org = org
        self.client = httpx.Client(
            base_url=url, headers={"Authorization": f"Token {token}"}, timeout=10
        )
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

    def _check_token(self):
        """Checks if the entered credential works"""
        response = self.client.get("/")
        if response.status_code != 200:
            raise ValueError(
                f"Check Parameters. Response Code: {response.status_code}. Message: {response.content}"
            )

    def emit(self, record):
        log = self.format(record)
        self.client.post(
            "/api/v2/write",
            params={"bucket": self.bucket_name, "org": self.org},
            data=log,
        )
