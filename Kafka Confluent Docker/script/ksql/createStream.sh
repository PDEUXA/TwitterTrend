#!/bin/bash
echo -e "\n\n⏳ Waiting for KSQL to be available before launching CLI\n"
while [ $(curl -s -o /dev/null -w %{http_code} http://ksqldb-server:8088/) -eq 000 ]
do
  echo -e $(date) "KSQL Server HTTP state: " $(curl -s -o /dev/null -w %{http_code} http://ksqldb-server:8088/) " (waiting for 200)"
  sleep 5
done

curl -X "POST" "http://ksqldb-server:8088/ksql" \
     -d $'{
  "ksql": "CREATE STREAM twitter_stream (id BIGINT, created_at STRING, tag STRING, lang STRING) WITH (kafka_topic=\'twitter\',timestamp=\'created_at\',timestamp_format=\'EEE MMM dd HH:mm:ss +0000 yyyy\', value_format=\'avro\');",
  "streamsProperties": {}
}'