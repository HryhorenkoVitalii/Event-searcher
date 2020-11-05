from Parsers.scraper import concert_artist


def get_artist_concerts(artist_code: str):
    concerts = concert_artist(artist_code)
