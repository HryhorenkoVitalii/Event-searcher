import os
from typing import Final, cast

from pydantic import BaseSettings


class LoggerConfig(BaseSettings):
    level: Final[str] = cast(str, os.environ.get("DEBUG_LEVEL"))

