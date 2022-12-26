from typing import Any

from pydantic import BaseModel


class DefaultResponse(BaseModel):
    success: bool
    payload: list[Any]
