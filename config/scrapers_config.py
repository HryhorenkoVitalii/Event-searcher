import os
from typing import Final, cast

from pydantic import BaseSettings


class ScrapersConfig(BaseSettings):
    request_attempts: Final[int] = int(cast(int, os.environ.get("REQUEST_ATTEMPTS")))
    request_timeout: Final[int] = int(cast(int, os.environ.get("REQUEST_TIMEOUT")))
    request_headers: Final[str | None] = cast(str | None, os.environ.get("REQUEST_HEADERS"))
    proxy:  Final[str | None] = cast(str | None, os.environ.get("PROXY"))
