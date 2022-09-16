

class Config:

    PROXY_WEBPAGE = "https://free-proxy-list.net/"

    TESTING_URL = "https://google.com"

    REDIS_CONFIG = {
        "host": "redis",
        "port": "6379",
        "db": 0
    }

    REDIS_KEY = "proxies"

    MAX_WORKERS = 100

    NUMBER_OF_PROXIES = 100

    RSS_FEEDS = {
        "en": [
            "https://www.mirror.co.uk/sport/?service=rss"

        ]
    }

    BOOTSTRAP_SERVERS = ["broker:9092"]

    TOPIC = "rss_news"

    VALIDATOR_CONFIG = {
        "description_length": 10,
        "languages": [
            "en", "pl", "es", "de"
        ]
    }
