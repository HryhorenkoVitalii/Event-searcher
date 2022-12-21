from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class ArtistData():
    name: str
    artist_code: str
    picture_url: str

@dataclass(frozen=True)
class ConcertData():
    name: str
    url: str
    date: str
    city: str
    country: str
