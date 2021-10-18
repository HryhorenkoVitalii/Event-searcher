from scrapers import songkick_scraper
from loguru import logger

#todo write tests
@logger.catch
def a():
    artist_code = "30543-matchbox-twenty"
    artist_code = "10068072-madona"
    location = "Kyiv"
    # concert_code = "/concerts/39791213-lindsey-stirling-at-national-palace-of-arts-ukraina"
    scraper = songkick_scraper.SongkickScraper()
    # print(scraper.concert_artist())
    print(scraper.search_location(location))

a()