from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from Myparser import WebParser
from log import log


@dataclass # this decorator will automatically add required dunder methods such as __init__ (for detail explanation https://docs.python.org/3/library/dataclasses.html)
class ProxyRecord:
    ip_address: str
    port: int
    country_code: str
    country: str
    anonymity: str
    google: str
    https: str
    last_checked: str
    proxy: dict = field(init=False, default=None) # init=False Do not pass in this attribute in the constructor argument

    def __post_init__(self):
        self.proxy = self.format_proxy() # proxy: dict will initialize here

    def format_proxy(self): # self explanatory
        protocol = "https" if self.https == "yes" else "http"
        url = f"{protocol}://{self.ip_address}:{self.port}"
        return {"http": url, "https": url}


@log
class ProxyPoolScraper:
    def __init__(self, url, bs_parser="lxml"): #reference https://lxml.de/
        self.parser = WebParser(url)
        self.bs_parser = bs_parser

    def get_proxy_stream(self, limit):
        raw_records = self.extract_table_raw_records()
        clean_records = list(
            map(self._clear_up_record, raw_records) # map(fun , iter)
        )
        for record in clean_records[1:limit]:
            self.log.info(f"Proxy record: {record}")
            if record:
                yield ProxyRecord(*record)

    def extract_table_raw_records(self):
        content = self.parser.get_content() #get all content gibberish form
        soup_object = BeautifulSoup(content, self.bs_parser) #arrange in proper sequence
        a = soup_object.find(id="list") #find <id="list"> inside html dom
        b = a.find_all('tr') # will find all <rt> tag in hierarchy
        return (b)

    def _clear_up_record(self, raw_record):
        return [
            val.text for val
            in raw_record.find_all("td") #will find every <td> tag inside every <tr> tag
        ]



#a = ProxyPoolScraper("https://free-proxy-list.net/")
#for value in a.get_proxy_stream(50):
#    print(value)

