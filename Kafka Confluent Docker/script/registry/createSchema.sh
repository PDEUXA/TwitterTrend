#!/bin/bash

SCHEMA_NAME="twitter-value"
SCHEMA_FILE="/usr/script/registry/avroValueSchema.avsc"

DATA={\"schema\":\"$(cat $SCHEMA_FILE | tr "\r\n" " " | tr -d " " | sed 's/"/\\"/g')\"}
printf "Create Schema %s with file %s " $SCHEMA_NAME $SCHEMA_FILE

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data $DATA http://schema-registry:8081/subjects/$SCHEMA_NAME/versions

printf "\nSchema :"
curl -X GET http://schema-registry:8081/subjects/$SCHEMA_NAME/versions/latest