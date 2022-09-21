FROM confluentinc/cp-kafka-connect-base:7.1.1

RUN confluent-hub install --no-prompt mongodb/kafka-connect-mongodb:latest \
    && confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:14.0.0


ENV CONNECT_PLUGIN_PATH="/usr/share/java,/usr/share/confluent-hub-components"

COPY connectors /etc/kafka-connect/connectors

WORKDIR /etc/kafka-connect/connectors

#RUN chmod +x ./register_connectors.sh

CMD ["./register_connectors.sh"]