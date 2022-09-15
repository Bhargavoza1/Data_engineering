''' this class will help us to validate our all proxy ip address '''

import time
from dataclasses import dataclass
from Myparser import WebParser
from log import log


@dataclass(frozen=True) # emulating immutability in python
class ProxyStatus:
    proxy: str
    health: float
    is_valid: bool


@log
class ProxyPoolValidator:
    def __init__(self, url, timeout=10, checks=3, sleep_interval=0.1):
        self.timeout = timeout
        self.checks = checks
        self.sleep_interval = sleep_interval
        self.parser = WebParser(url, rotate_header=True)

    def validate_proxy(self, proxy_record):# this method every time will call to the get_content inside web_parser
        consecutive_checks = []
        for _ in range(self.checks):
            content = self.parser.get_content(
                timeout=self.timeout,
                proxies=proxy_record.proxy
            )
            time.sleep(self.sleep_interval)
            consecutive_checks.append(int(content is not None))

        health = sum(consecutive_checks) / self.checks
        proxy_status = ProxyStatus(
            proxy=proxy_record.proxy,
            health=health,
            is_valid=health > 0.66
        )
        self.log.info(f"Proxy status: {proxy_status}")
        return proxy_status



#a = ProxyPoolValidator("https://google.com")
#from proxypool import  proxypool_scraper
#b = proxypool_scraper.ProxyPoolScraper("https://free-proxy-list.net/")
#c = b.get_proxy_stream(50)

'''#this is simpler way to validate proxy
 will take too much time to finish'''
#for value in b.get_proxy_stream(50):
#    a.validate_proxy(value)

'''#this will run on Thread. but work as above'''

#from concurrent.futures import ThreadPoolExecutor # The asynchronous execution can be performed with threads
#with ThreadPoolExecutor(max_workers=50) as executor: # refer -> https://docs.python.org/3/library/concurrent.futures.html
#    results = executor.map(
#        a.validate_proxy, c
#    )

