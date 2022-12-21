from entities import ArtistData, ConcertData
from interface import ApiInterface

class Action(ApiInterface):

    def get_artists(self, artist_name: str) -> list[ArtistData]:
        result: list[ArtistData]= []

        return result
    
    def get_concerts(self, artist_name: str) -> list[ConcertData]:
        result: list[ConcertData]= []

        return result