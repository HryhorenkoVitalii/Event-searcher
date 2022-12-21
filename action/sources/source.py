from scrapers import SongkickScraper
from interface import ApiInterface

class Source(ApiInterface):

    def __init__(self) -> None:
        self.soundkick = SongkickScraper()

    def get_artists(self, artist_name):
        soundkick_artists = self.soundkick.get_artists(artist_name)
        return soundkick_artists
    
    def get_concerts(self, artist_code):
        soundkick_concert = self.soundkick.get_concerts(artist_code)
        return soundkick_concert
    
