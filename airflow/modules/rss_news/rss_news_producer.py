import re
from dataclasses import dataclass
import atoma #Atom, RSS and JSON feed parser for Python 3.
from modules import WebParser


@dataclass(frozen=True)# emulating immutability in python
class News:
    _id: str
    title: str
    link: str
    published: str
    description: str
    author: str
    language: str

    def as_dict(self):
        return self.__dict__


class NewsProducer:
    def __init__(self, rss_feed, language):
        self.parser = WebParser(rss_feed, rotate_header=True)
        self.formatter = NewsFormatter(language)

    def _extract_news_feed_items(self, proxies):
        content = self.parser.get_content(proxies=proxies)
        #content = self.parser.get_content( )
        news_feed = atoma.parse_rss_bytes(content) # kind of creating our rss feed into array form
        return news_feed.items

    def get_news_stream(self, proxies):
        news_feed_items = self._extract_news_feed_items(proxies)# this method will extract all rssitem from rss feed
        for entry in news_feed_items:
            formatted_entry = self.formatter.format_entry(entry)
            yield formatted_entry


class NewsFormatter:
    def __init__(self, language):
        self.language = language
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.id_regex = "[^0-9a-zA-Z_-]+"
        self.default_author = "Unknown"

    def format_entry(self, entry):
        description = self.format_description(entry)
        return News(
            self.construct_id(entry.title),
            entry.title,
            entry.link,
            self.unify_date(entry.pub_date),
            description,
            self.assign_author(entry.author),
            self.language
        )

    def construct_id(self, title):
        return re.sub(self.id_regex, "", title).lower()# removing every space and special characters from news tital. and creating id from it

    def unify_date(self, date):
        a = date.strftime(self.date_format)
        return date.strftime(self.date_format) #returns a string representing date and time using date, time

    def assign_author(self, author):
        return self.default_author if not author else author

    def format_description(self, entry):
        tmp_description = re.sub("<.*?>", "", entry.description[:1000])#find every remaining html tag and remove it within 1000 character.
        index = tmp_description.rfind(".") # last occurrence of the specified value
        short_description = tmp_description[:index+1]
        return (
            short_description if short_description
            else entry.title
        )






#<editor-fold desc=" testing  ">
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
''' ''' if you want to test on proxy remove this comments and start redis docker 

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
for n, item in enumerate(RSS_FEEDS.items()):
    language, rss_feeds = item
    print(rss_feeds[0])
    producer = NewsProducer(rss_feeds[0], language)
    #redis = rpc.RedisProxyPoolClient(rpc.REDIS_KEY , rpc.REDIS_CONFIG)  #remove this comments as well
    #proxy = redis.get_proxy()
    proxy =None
    for news in producer.get_news_stream(proxy):
        a = news
        print(a)
'''
#</editor-fold>