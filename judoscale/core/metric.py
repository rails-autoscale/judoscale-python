import logging
import re
import time
from dataclasses import dataclass
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class Metric:
    timestamp: int
    value: float
    queue_name: str = None
    measurement: str = "queue_time"

    @property
    def as_tuple(self) -> Tuple[int, float, str, str]:
        """
        Return a tuple of the metric's timestamp, value, measurement and queue.
        """
        return (
            round(self.timestamp),
            round(self.value, 2),
            self.measurement,
            self.queue_name,
        )

    @classmethod
    def for_web(cls, header_value: str) -> Optional["Metric"]:
        """
        Parse the X-Request-Start header value and return a Metric instance.

        Removes non-digits:
            This removes the "t=" prefix added by some web servers (NGINX).
        Removes decimal:
            NGINX also reports this time as fractional seconds with millisecond
            resolution, so removing the decimal gives us integer milliseconds
            (same as Heroku).

        Calculate how long a request has been waiting to be handled, log and
        return a Metric instance.
        """
        request_start = re.sub(r"\D", "", header_value)

        if len(request_start) == 0:
            return None

        logger.debug(f"START X {request_start}")
        now = time.time()
        latency = max(0, now * 1000 - int(request_start))
        logger.debug(f"queue_time={latency:.2f}ms")
        return Metric(timestamp=now, value=latency, measurement="queue_time")
