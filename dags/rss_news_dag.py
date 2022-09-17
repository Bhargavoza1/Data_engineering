from urllib.parse import urlparse
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from dags_config import Config as config
from custom_operators import (
    ProxyPoolOperator,
    RSSNewsOperator
)


def extract_feed_name(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc.replace("www.", "") # netloc Contains the network location - which includes the domain itself and remove www. char


def dummy_callable(action):
    return f"{datetime.now()}: {action} scrapping RSS feeds!"


def export_events(config, rss_feed, language, dag):
    feed_name = extract_feed_name(rss_feed)
    return RSSNewsOperator(
        task_id=f"exporting_{feed_name}_news_to_broker",
        validator_config=config.VALIDATOR_CONFIG,
        rss_feed=rss_feed,
        language=language,
        redis_config=config.REDIS_CONFIG,
        redis_key=config.REDIS_KEY,
        bootstrap_servers=config.BOOTSTRAP_SERVERS,
        topic=config.TOPIC,
        dag=dag
    )


def create_dag(dag_id, interval, config, language, rss_feeds):
    with DAG(
        dag_id=dag_id,
        description=f"Scrape latest ({language}) sport RSS feeds",
        schedule_interval=interval,
        start_date=datetime(2020, 1, 1),
        catchup=False,
        is_paused_upon_creation=False
    ) as dag:

        #dummy task to know if dag started
        start = PythonOperator(
            task_id="starting_pipeline",
            python_callable=dummy_callable,
            op_kwargs={"action": "starting"},
            dag=dag
        )

        #scraping proxy and pushing it to redis
        proxypool = ProxyPoolOperator(
            task_id="updating_proxypoool",
            proxy_webpage=config.PROXY_WEBPAGE,
            number_of_proxies=config.NUMBER_OF_PROXIES,
            testing_url=config.TESTING_URL,
            max_workers=config.NUMBER_OF_PROXIES,
            redis_config=config.REDIS_CONFIG,
            redis_key=config.REDIS_KEY,
            dag=dag
        )
        # n = rss_feeds
        #create n number of tasks
        events = [
            export_events(config, rss_feed, language, dag)
            for rss_feed in rss_feeds
        ]
        # dummy task to know if dag is finished
        finish = PythonOperator(
            task_id="finishing_pipeline",
            python_callable=dummy_callable,
            op_kwargs={"action": "finishing"},
            dag=dag
        )

        start >> proxypool >> events >> finish

    return dag


for n, item in enumerate(config.RSS_FEEDS.items()):
    language, rss_feeds = item # rss_feeds as array
    dag_id = f"rss_news_{language}" # assigning dag id with RSS_FEEDS dictionary key
    interval = f"{n*4}-59/10 * * * *" # Cron job interval #refer  https://crontab.guru/

    # creat n number of dag
    globals()[dag_id] = create_dag(
        dag_id,
        interval,
        config, # dags_config.py file
        language,
        rss_feeds
    )
