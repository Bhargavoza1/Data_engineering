
import re
import random
from contextlib import closing
from requests import get
from modules import log
from modules.Myparser.random_headers_list import headers_list


@log
class WebParser:
    def __init__(self, website_url, rotate_header=True): # constructor
        self.url = website_url
        self._rotate_header = rotate_header

    def get_random_header(self):
        if self._rotate_header:
            return random.choice(headers_list) # self explanatory will get random header list from random_headers_list file

    def get_content(self, timeout=30, proxies=None):
        kwargs = {
            "timeout": timeout,
            "proxies": proxies,
            "headers": self.get_random_header()
        }
        try: # requests.get we are passing custom kwargs and mainly headers
            with closing(get(self.url, **kwargs)) as response: # Return a context manager that closes thing upon completion of the block
                if self.is_good_response(response): #   on success response 200 will return of that pages
                    return (
                        response.content
                    )
        except Exception as err:
            self.log.info(f"Error occurred: {err}")

    @staticmethod
    def is_good_response(response):
        content_type = response.headers['Content-Type'].lower()
        return (
            response.status_code == 200
            and content_type is not None
        )

    def __str__(self):
        domain = re.sub("(http[s]?://|www.)", "", self.url) # convert https://www.google.co.in/ -> GOOGLE.CO.IN
        return f"WebParser of {domain.upper()}"


#a = WebParser("https://www.eyefootball.com/football_news.xml")
#b = a.get_content()
#
#str(a)

