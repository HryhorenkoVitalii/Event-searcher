from .default import DefaultResponse
from pydantic import BaseModel

class ArtistDataResponse(BaseModel):
    name: str
    soundkick_code: str
    picture_url: str

class ConcertDataResponse(BaseModel):
    name: str
    url: str
    date: str
    city: str
    country: str

class DefaultApiResponse(DefaultResponse):
    payload: list[ArtistDataResponse] or list[ConcertDataResponse]
