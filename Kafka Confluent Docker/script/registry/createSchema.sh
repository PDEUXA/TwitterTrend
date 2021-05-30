#!/bin/bash

SCHEMA_NAME="twitter-value"
SCHEMA_FILE="/usr/script/registry/avroValueSchema.avsc"

echo -e "\n\n⏳ Waiting for Registry to be available   \n"
while [ $(curl -s -o /dev/null -w %{http_code} http://schema-registry:8081/) -eq 000 ]
do
  echo -e $(date) "Registry Server HTTP state: " $(curl -s -o /dev/null -w %{http_code} http://schema-registry:8088/) " (waiting for 200)"
  sleep 5
done

DATA={\"schema\":\"$(cat $SCHEMA_FILE | tr "\r\n" " " | tr -d " " | sed 's/"/\\"/g')\"}
printf "Create Schema %s with file %s " $SCHEMA_NAME $SCHEMA_FILE

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data $DATA http://schema-registry:8081/subjects/$SCHEMA_NAME/versions

printf "\nSchema :"
curl -X GET http://schema-registry:8081/subjects/$SCHEMA_NAME/versions/latest