#!/bin/bash

docker-compose exec schema-registry bash /usr/script/registry/createSchema.sh
docker-compose exec broker bash /usr/script/broker/createTopic.sh
docker-compose exec ksqldb-server bash /usr/script/ksql/createStream.sh
docker-compose exec ksqldb-server bash /usr/script/ksql/createTable.sh
docker-compose exec connect bash /usr/script/connect/addMongoConnector.sh


docker-compose exec nifi-worker bash /home/nifi/conf/registry/startup_conf.sh