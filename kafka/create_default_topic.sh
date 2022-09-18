#!/bin/sh

/etc/confluent/docker/run &
echo -e "Waiting for Kafka to start listening on localhost"

kafka-topics --create --if-not-exists \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1 \
    --topic rss_news

sleep infinity