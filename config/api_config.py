import os
from typing import Final, cast

from pydantic import BaseSettings


class ApiConfig(BaseSettings):
    title: Final[str] = cast(str, os.environ.get("TITLE"))
    host: Final[str] = cast(str, os.environ.get("HOST"))
    port: Final[int] = int(cast(int, os.environ.get("PORT")))
    docs_url: Final[str | None] = cast(str | None, os.environ.get("DOCS_URL"))
    openapi_url: Final[str | None] = cast(str | None, os.environ.get("OPENAPI_URL"))
    redoc_url: Final[str | None] = cast(str | None, os.environ.get("REDOC_URL"))
