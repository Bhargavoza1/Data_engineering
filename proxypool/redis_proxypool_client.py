''' before debugging/testing this we have to create docker image for the redis
*** docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest ***
use above command to creat docker instance of redis'''


import json
import redis
from log import log

#<editor-fold desc=" redis config for local use and testing only ">

REDIS_CONFIG = {
    "host": "localhost",
    "port": "6379",
    "db": 0
}

REDIS_KEY = "proxies"

#</editor-fold>

@log
class RedisProxyPoolClient:
    def __init__(self, key, redis_config):
        self.key = key
        self.redis = redis.Redis(
            **redis_config
        )

    def __enter__(self):
        return self

    def override_existing_proxies(self, proxies):
        self.log.info(f"Overriding existing proxies {proxies}")
        self.redis.delete(self.key)
        self.redis.lpush(self.key, *proxies)

    def list_existing_proxies(self): # get json value from redis
        response = self.redis.lrange(self.key, 0, -1)
        return [
            json.loads(proxy) for proxy in response
        ]

    def get_proxy(self):
        existing_proxies = self.list_existing_proxies()
        if len(existing_proxies) > 0:
            return existing_proxies[0]

    def lpop_proxy(self):
        self.log.info("Deleting proxy!")
        self.redis.lpop(self.key)

    def __exit__(self, type, value, traceback):
        client_id = self.redis.client_id()
        self.redis.client_kill_filter(
            _id=client_id
        )



#<editor-fold desc=" testing  ">
'''
from proxypool import proxypool_validator
a = proxypool_validator.ProxyPoolValidator("https://google.com")
from proxypool import  proxypool_scraper
b = proxypool_scraper.ProxyPoolScraper("https://free-proxy-list.net/")
c = b.get_proxy_stream(50)



from concurrent.futures import ThreadPoolExecutor # The asynchronous execution can be performed with threads
with ThreadPoolExecutor(max_workers=50) as executor: # refer -> https://docs.python.org/3/library/concurrent.futures.html
    results = executor.map(
        a.validate_proxy, c
    )
    valid_proxies = filter(lambda x: x.is_valid is True, results)
    sorted_valid_proxies = sorted(
        valid_proxies, key=lambda x: x.health, reverse=True
    )

with RedisProxyPoolClient(REDIS_KEY , REDIS_CONFIG) as client:
   client.override_existing_proxies(
       [
           json.dumps(record.proxy)
           for record in sorted_valid_proxies[:5]
       ]
   )


rds = redis.Redis(host='localhost', port=6379)
rds.set("bb","aa")
rds.get("bb")

prx =  rds.lrange(REDIS_KEY, 0, -1)
listprx = [json.loads(proxy) for proxy in prx]
print(listprx[0])
'''
#</editor-fold>