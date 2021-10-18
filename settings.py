##Database settings

#setting psql
PSQL_CREDENTIAL = ''
PSQL_TABLE_NAME = "event_scraper_back"
PSQL_TABLE_STRUCTURE = """request_from TEXT,
                          id TEXT,
                          request_type TEXT,
                          request_data TEXT,
                          datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                          """


##Scraper settings

#setting request
REQUEST_ATTEMPTS:int = 10
REQUEST_HEADERS:str  = None
REQUEST_TIMEOUT:int = 10
PROXY:str = None


##Other settings
DEBUG_LEVEL:str = "DEBUG"

##Api settings
X_API_KEY = {"Main password": "password"}