from Parsers.scraper import concert_artist


def get_artist_concerts(code: str):
    concerts = concert_artist(code)
