#!/bin/bash
CONNECTOR_CONFIG="/usr/script/connect/Kafka2MongoConfig.json"
#CONNECTOR_CONFIG="Kafka2MongoConfig.json"
#DATA=\'$(cat $CONNECTOR_CONFIG| tr "\r\n" " " | tr -d " " )\'
#
#confluent-hub install mongodb/kafka-connect-mongodb:1.5.0 --no-prompt
echo "Waiting for Kafka Connect to start listening on kafka-connect ⏳"
while [ $(curl -s -o /dev/null -w %{http_code} http://connect:8083/connectors) -eq 000 ] ; do
  echo -e $(date) " Kafka Connect listener HTTP state: " $(curl -s -o /dev/null -w %{http_code} http://connect:8083/connectors) " (waiting for 200)"
  sleep 5
done


printf "Create Connector with config %s \n" $CONNECTOR_CONFIG
curl -X POST -H "Content-Type: application/json"  --data @$CONNECTOR_CONFIG http://connect:8083/connectors

