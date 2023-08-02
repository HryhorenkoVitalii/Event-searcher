from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel, Field

@dataclass(frozen=True)
class ArtistData():
    id: int
    name: str
    soundkick_code: str
    picture_url: str
    last_update: datetime

@dataclass(frozen=True)
class ConcertData():
    id: int
    name: str
    url: str
    date: str
    concert_hall: str
    city: str


class ClientRequest(BaseModel):
    # id: str|None
    source: str|None = Field(examples= ["fapl]"])
    date_last_use: datetime = datetime.now()
    request: str|None
