from typing import Protocol

class ApiInterface(Protocol):

    def get_artists(self, artist_name: str):pass
    
    def get_concerts(self, artist_name: str):pass
