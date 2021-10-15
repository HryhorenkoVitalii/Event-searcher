##Database settings

#setting psql
PSQL_CREDENTIAL = 'postgresql://postgres:sacred@localhost:5432/postgres'
PSQL_TABLE_NAME = ""
PSQL_TABLE_STRUCTURE = ""


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