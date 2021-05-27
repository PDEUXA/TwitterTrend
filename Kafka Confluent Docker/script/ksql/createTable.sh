#!/bin/bash
echo -e "\n\n⏳ Waiting for KSQL to be available before launching CLI\n"
while [ $(curl -s -o /dev/null -w %{http_code} http://ksqldb-server:8088/) -eq 000 ]
do
  echo -e $(date) "KSQL Server HTTP state: " $(curl -s -o /dev/null -w %{http_code} http://ksqldb-server:8088/) " (waiting for 200)"
  sleep 5
done
curl -X POST -H "Content-Type: application/vnd.ksql.v1+json" \
--data $'{"ksql":"CREATE TABLE HASHTAG_COUNT_1HR AS SELECT tag as hashtag, COUNT(*) as nb_hash,TIMESTAMPTOSTRING(WINDOWSTART, \'yyyy-MM-dd HH:mm:ss.SSS\')  as window_start, TIMESTAMPTOSTRING(WINDOWEND, \'yyyy-MM-dd HH:mm:ss.SSS\') as window_end, AS_VALUE(tag) as tag_name, \'stream\' as origine FROM twitter_stream WINDOW TUMBLING (SIZE 1 HOUR,  RETENTION 2 HOURS, GRACE PERIOD 2 MINUTES) GROUP BY tag EMIT CHANGES;"}' \
 "http://ksqldb-server:8088/ksql"
