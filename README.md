
<h1 align="center">
   <br>
  <a><img src="https://kidfromthe6ix.files.wordpress.com/2014/10/concert-crowd-fireworks-gif-lights-favim-com-292862.gif" width="250"></a>
  <br>
  <br>
  Evants scraper back
  <br>
</h1>

<h4 align="center">The Evants scraper backend</h4>
The scraper with REST interface for scraping concerts 

### start
For start server you need run app.py, beforehand setting up postgres credential at settings.py

### API endpoints
For all requests need send X-API-KEY in headers - default X-API-KEY = password
```bash
# [GET] to search the artist for artist name.
# Structure responce [{Name: Artist name, 
#                      Artist code: artist code, 
#                      Picture url: picture url}, ...]
# Responce can have multiple dicts
/<request_from>/<id>/search_artist/?Artist name=<Artist name>

# [GET] to search events for artist code.
# Structure responce [{Link: Link,
#                      Date: Date,
#                      Concert hall: concert hall,
#                      Place: concert place}), ...]
# Responce can have multiple dicts
/<request_from>/<id>/search_events/?Artist code=<Artist code>

# [GET] to get link for buy ticet on event.
# Structure responce {Ticket url: ticker url}
/<request_from>/<id>/get_ticket/?Concert Link=<Concert Link>
```

## Credits

This software uses the following open source packages:

- [Flask](https://flask.palletsprojects.com/)
- [Loguru](https://loguru.readthedocs.io/)
- [Psycopg2](https://www.psycopg.org/)
