from .default import DefaultResponse
from pydantic import BaseModel

class ArtistDataResponse(BaseModel):
    id: int
    name: str
    soundkick_code: str
    picture_url: str

class ConcertDataResponse(BaseModel):
    name: str
    url: str
    date: str
    city: str
    concert_hall: str

class DefaultApiResponse(DefaultResponse):
    payload: list[ArtistDataResponse] | list[ConcertDataResponse]
