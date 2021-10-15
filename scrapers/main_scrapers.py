from scrapers.songkick_scraper import SongkickScraper


class MainScrapers():

    def __init__(self) -> None:
        self.soundkick = SongkickScraper()

    def get_artist(self, artist_name):
        soundkick_artists = self.soundkick.get_artist(artist_name)
        return soundkick_artists
    
    def get_concert(self, artist_code):
        soundkick_concert = self.soundkick.get_concert(artist_code)
        return soundkick_concert
    
    def get_ticket(self, concert_code):
        ticket_url = self.soundkick.get_ticket(concert_code)
        return ticket_url