# InfluxDB Logging Handler

## Usage

```python
import os
import logging

from influxdb_logger import InfluxHandler

logger = logging.getLogger()
influx_handler = InfluxHandler(
    url=os.environ["INFLUXDB_URL"],
    token=os.environ["INFLUXDB_TOKEN"],
    org=os.environ["INFLUXDB_ORG"],
    tag_key="location",
    tag_value="iot_dashboard",
    bucket_name=os.environ["INFLUXDB_LOGGING_BUCKET"],
)
logger.setLevel(logging.DEBUG)
logger.addHandler(influx_handler)
```