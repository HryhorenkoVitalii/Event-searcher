import os
from typing import Final, cast

from pydantic_settings import BaseSettings


class ScrapersConfig(BaseSettings):
    request_attempts: Final[int] = int(cast(int, os.environ.get("SCRAPERS_REQUEST_ATTEMPTS")))
    request_timeout: Final[int] = int(cast(int, os.environ.get("SCRAPERS_REQUEST_TIMEOUT")))
    request_headers: Final[str | None] = cast(str | None, os.environ.get("SCRAPERS_REQUEST_HEADERS", None))
    request_proxy:  Final[str | None] = cast(str | None, os.environ.get("SCRAPERS_PROXY", None))
