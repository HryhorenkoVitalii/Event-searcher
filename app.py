from flask import Flask, jsonify, request
from functools import wraps
from settings  import X_API_KEY
from scrapers.main_scrapers import MainScrapers
from loguru import logger as api_logger
from dbs_manage import PsqlManagment
from settings import DEBUG_LEVEL, PSQL_CREDENTIAL, PSQL_TABLE_NAME, PSQL_TABLE_STRUCTURE


event_scraper_api = Flask("NewsBot")
scraper = MainScrapers()
psql_manages = PsqlManagment(PSQL_CREDENTIAL)
api_logger.add('logs/api/logs.log', level=DEBUG_LEVEL)

def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-api-key') and request.headers.get('X-api-key') in X_API_KEY.values():
            return view_function(*args, **kwargs)
        else:
            return jsonify({"Message": "Api key is invalid"}), 403
    return decorated_function

def create_psql_table(table_name, table_structure):
    query = f"""CREATE IF NOT EXIST TABLE {table_name} 
                ({table_structure})"""
    psql_manages.execute_psql_query(query)

def save_request_to_db(request_from, id, data):
    psql_manages.write_to_db([request_from, id, ])


@event_scraper_api.route("/search_artist/<request_from>/<id>/", methods=["GET"])
@require_appkey
def get_artist():
    artist_name = request.args.get('Artist name')
    artist_name_list = scraper.get_artist(artist_name)
    if artist_name_list:
        return jsonify(artist_name_list)
    else:
        return jsonify({"Message": "Name not found"}), 404


@event_scraper_api.route("/search_events/<request_from>/<id>/", methods=["GET"])
@require_appkey
def get_events(artist_code:str):
    artist_code = request.args.get('Artist code')
    concert_list = scraper.get_concert(artist_code)
    if concert_list["In tour"]:
        return jsonify(concert_list)
    else:
        return jsonify({"Message": "Events not found"}), 404

@event_scraper_api.route("/get_ticket/<request_from>/<id>/", methods=["GET"])
@require_appkey
def get_ticket():
    concert_url = request.args.get('Concert url')
    ticker_url = scraper.get_ticket(concert_url)
    if ticker_url:
        return jsonify({"Ticket url": ticker_url})
    else:
        return jsonify({"Message": "Ticket not found"}), 404


def run_server():
    create_psql_table(PSQL_TABLE_NAME, PSQL_TABLE_STRUCTURE)
    event_scraper_api.run()

if __name__ == "__main__":
    run_server()