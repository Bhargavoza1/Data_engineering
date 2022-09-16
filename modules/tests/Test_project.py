from modules import proxypool_validator
from modules import  proxypool_scraper
from modules import rss_news_producer
from modules import NewsExporter
from modules import NewsValidator


RSS_FEEDS = {
        "en": [
            "https://www.mirror.co.uk/sport/?service=rss"
        ]
    }

VALIDATOR_CONFIG = {
        "description_length": 10,
        "languages": [
            "en", "pl", "es", "de"
        ]
    }

a = proxypool_validator.ProxyPoolValidator("https://google.com")

b = proxypool_scraper.ProxyPoolScraper("https://free-proxy-list.net/")
c = b.get_proxy_stream(100)



from concurrent.futures import ThreadPoolExecutor # The asynchronous execution can be performed with threads
'''  if you want to test on proxy remove this comments and start redis docker

with ThreadPoolExecutor(max_workers=100) as executor: # refer -> https://docs.python.org/3/library/concurrent.futures.html
    results = executor.map(
        a.validate_proxy, c
    )
    valid_proxies = filter(lambda x: x.is_valid is True, results)
    sorted_valid_proxies = sorted(
        valid_proxies, key=lambda x: x.health, reverse=True
    )

import json
from proxypool import  redis_proxypool_client as rpc

with rpc.RedisProxyPoolClient(rpc.REDIS_KEY , rpc.REDIS_CONFIG) as client:
   client.override_existing_proxies(
       [
           json.dumps(record.proxy)
           for record in sorted_valid_proxies[:]
       ]
   )
'''

#this given below code push our rss data to kafka topic
with NewsExporter(['localhost:9092']) as exporter:

    for n, item in enumerate(RSS_FEEDS.items()):
        language, rss_feeds = item
        producer = rss_news_producer.NewsProducer(rss_feeds[0], language)
        validator = NewsValidator(VALIDATOR_CONFIG)
        #redis = rpc.RedisProxyPoolClient(rpc.REDIS_KEY , rpc.REDIS_CONFIG)  #remove this comments as well
        #proxy = redis.get_proxy()
        proxy =None
        for news in producer.get_news_stream(proxy):
            validator.validate_news(news)
            exporter.export_news_to_broker(
                'rss_news',
                news.as_dict()
            )
