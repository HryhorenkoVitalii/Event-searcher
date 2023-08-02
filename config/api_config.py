import os
from typing import Final, cast

from pydantic_settings import BaseSettings


class ApiConfig(BaseSettings):
    title: Final[str] = cast(str, os.environ.get("API_TITLE"))
    host: Final[str] = cast(str, os.environ.get("API_HOST"))
    port: Final[int] = int(cast(int, os.environ.get("API_PORT")))
    docs_url: Final[str | None] = cast(str | None, os.environ.get("API_DOCS_URL", None))
    openapi_url: Final[str | None] = cast(str | None, os.environ.get("API_OPENAPI_URL", None))
    redoc_url: Final[str | None] = cast(str | None, os.environ.get("API_REDOC_URL", None))
