import json
import time
from kafka import KafkaProducer


class NewsExporter:
    def __init__(self, bootstrap_servers):
        self._producer = self._connect_producer(
            bootstrap_servers
        )

    def _connect_producer(self, bootstrap_servers):
        def encode_news(value):
            return json.dumps(value).encode("utf-8")

        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: encode_news(x)
        )
        return producer

    def __enter__(self):
        return self

    def export_news_to_broker(self, topic, record, sleep_time=0.01):
        response = self._producer.send(
            topic,
            value=record
        )
        time.sleep(sleep_time)
        return response.get(
            timeout=60
        )

    def __exit__(self, type, value, traceback):
        self._producer.close()




# <editor-fold desc=" testing  ">
''' 

RSS_FEEDS = {
        "en": [
            "https://www.mirror.co.uk/sport/?service=rss"
        ]
    }


from proxypool import proxypool_validator
a = proxypool_validator.ProxyPoolValidator("https://google.com")
from proxypool import  proxypool_scraper
b = proxypool_scraper.ProxyPoolScraper("https://free-proxy-list.net/")
c = b.get_proxy_stream(100)



from concurrent.futures import ThreadPoolExecutor # The asynchronous execution can be performed with threads
''' '''  if you want to test on proxy remove this comments and start redis docker

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
''''''
from rss_news import rss_news_producer
#this given below code push our rss data to kafka topic
with NewsExporter(['localhost:9092']) as exporter:

    for n, item in enumerate(RSS_FEEDS.items()):
        language, rss_feeds = item
        producer = rss_news_producer.NewsProducer(rss_feeds[0], language)
        #redis = rpc.RedisProxyPoolClient(rpc.REDIS_KEY , rpc.REDIS_CONFIG)  #remove this comments as well
        #proxy = redis.get_proxy()
        proxy =None
        for news in producer.get_news_stream(proxy):
            exporter.export_news_to_broker(
                'rss_news',
                news.as_dict()
            )
'''
# </editor-fold>

