import os
from typing import Final, cast

from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):    
    psql_credential: Final[str] = cast(str, os.environ.get("PSQL_CREDENTIAL"))

