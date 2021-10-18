from abc import ABC, abstractclassmethod
from requests.exceptions import SSLError, ProxyError, Timeout, ConnectionError
import requests
from settings import *
from dbs_manage import PsqlManagment
from collections import defaultdict
from loguru import logger as scraper_logger
from bs4 import BeautifulSoup


scraper_logger.add('logs/scrapers/logs.log', level=DEBUG_LEVEL)

class AbstractScraper(ABC):

        def __init__(self, logger=scraper_logger) -> None:
            self.psql_manages = PsqlManagment(PSQL_CREDENTIAL)
            self.request_attempt = REQUEST_ATTEMPTS
            self.COUNTERS = defaultdict(int)
            self.headers = REQUEST_HEADERS
            self.proxy = PROXY
            self.request_timeout = REQUEST_TIMEOUT
            self.logger = logger

        def _try_except_requests_handler(self, url, params, allow_redirects):
            try:
                self.COUNTERS["Total requests"] += 1
                resp = requests.get(
                                    url,
                                    headers=self.headers,
                                    params=params,
                                    timeout=self.request_timeout,
                                    proxies=self.proxy,
                                    allow_redirects=allow_redirects
                                    )
                return resp
            except SSLError:
                self.COUNTERS["Unsuccess requests"] += 1
                self.logger.error(f"Site Unavailable :: {url} :: SSL Error")
            except ProxyError:
                self.COUNTERS["Unsuccess requests"] += 1
                self.logger.error(f"Proxy error :: {url}")
                self.COUNTERS["Proxy error"] += 1
            except Timeout:
                self.COUNTERS["Unsuccess requests"] += 1
                self.logger.error(f"TimeOut ({self.timeout} sec) :: {url}")
            except ConnectionError:
                self.COUNTERS["Unsuccess requests"] += 1
                self.logger.error(f"ConnectionError :: {url}")
            except Exception as err:
                self.COUNTERS["Unsuccess requests"] += 1
                self.logger.error(f"Unknown error :: {url}, error: {err}")


        def get_request(self, url:str, params:str=None, 
                        allow_redirects:bool = True) -> dict:
            for _ in range(self.request_attempt):
                resp = self._try_except_requests_handler(url, params, allow_redirects)
                if resp:
                    if resp.status_code in [200]:
                        self.logger.success(f"Request is success :: {url}")
                        self.COUNTERS["Success requests"] += 1
                        return {"Request status": "Success",
                                "Data": resp}
                    elif resp.status_code in [403, 401]:  # FORBIDDEN OR PROXY BANNED -- TRY AGAIN WITH NEW PROXY
                        self.COUNTERS["Unsuccess requests"] += 1
                        self.logger.debug(
                            f"Request is Unsuccess :: status code {resp.status_code} :: {url}")
                        continue
                    elif resp.status_code in [404, 402]:
                        self.COUNTERS["Fail request"] += 1
                        self.logger.debug(
                            f"Site Unavailable :: status code {resp.status_code} :: {url}")
                        return {"Request status": "Error",
                                "Data": {"Status code": resp.status_code, "Message": "Site unavailable"}}
                    else:
                        self.logger.debug(
                            f"Unknown status code :: status code {resp.status_code} :: {url}")
                else:
                    continue
            self.logger.error(
                f"Fail request :: {url}, attempts requests are over\n{self.COUNTERS}")
            self.COUNTERS["Fail request"] += 1
            return {"Request status": "Error",
                    "Data": {"Code": "Attempts over", "Message": "Attempts requests are over"}}

        def get_soup(self, url):
            html_request = self.get_request(url)["Data"]
            soup = BeautifulSoup(html_request.text, 'lxml')
            return soup


if __name__ == '__main__':
    print("Abstract scraper module")