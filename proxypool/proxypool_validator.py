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

    def validate_proxy(self, proxy_record):
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


a = ProxyPoolValidator("https://google.com")
from proxypool import  proxypool_scraper
b = proxypool_scraper.ProxyPoolScraper("https://free-proxy-list.net/")
c = b.get_proxy_stream(50)

from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(
        a.validate_proxy, c
    )
    valid_proxies = filter(lambda x: x.is_valid is True, results)
    sorted_valid_proxies = sorted(
        valid_proxies, key=lambda x: x.health, reverse=True
    )
