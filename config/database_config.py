import os
from typing import Final, cast

from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    username: Final[str] = cast(str, os.environ.get("PSQL_USERNAME")),
    password: Final[str] = cast(str, os.environ.get("PSQL_PASSWORD"))
    host: Final[str] = cast(str, os.environ.get("PSQL_HOST")),
    database: Final[str] = cast(str, os.environ.get("PSQL_DATABASE")),    
