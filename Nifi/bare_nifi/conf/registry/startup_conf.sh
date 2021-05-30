#!/bin/sh
REGISTRY_CONF="/home/nifi/conf/registry/registry_conf.json"
TEMP="/home/nifi/conf/registry/temp.json"
echo "Waiting for Nifi to start listening  ⏳"
while [ $(curl -s -o /dev/null -w %{http_code} http://nifi-worker:8080/nifi-api) -eq 000 ]; do
  echo -e $(date) " Nifi listener HTTP state: " $(curl -s -o /dev/null -w %{http_code} http://nifi-worker:8080/nifi-api) " (waiting for 200)"
  sleep 5
done
ROOT_ID=$(curl -s -X GET -H "Content-Type: application/json" http://nifi-worker:8080/nifi-api/flow/process-groups/root | jq -r '.processGroupFlow.id')
echo "ROOT ID"$ROOT_ID

#jq --arg rootid "$ROOT_ID" '.revision.clientId |= $rootid' $REGISTRY_CONF > temp.json
REGISTRY_ID=$( curl -s -X POST -H "Content-Type: application/json" --data @$REGISTRY_CONF http://nifi-worker:8080/nifi-api/controller/registry-clients  | jq -r '.id')
echo "REGISTRY ID" $REGISTRY_ID

echo "Waiting for Nifi-Registry to start listening  ⏳"
while [ $(curl -s -o /dev/null -w %{http_code} http://nifi-registry:18080/nifi-registry-api/) -eq 000 ]; do
  echo -e $(date) " Nifi listener HTTP state: " $(curl -s -o /dev/null -w %{http_code} http://nifi-registry:18080/nifi-api) " (waiting for 200)"
  sleep 5
done

echo "Create bucket"
BUCKET_ID=$(curl -s -X POST -H "Content-Type: application/json" --data '{"name": "twitter_bucket"}' http://nifi-registry:18080/nifi-registry-api/buckets | jq -r '.identifier')
echo "BUCKET ID"$BUCKET_ID

echo "Create flow"
FLOW_ID=$(curl -s -X POST -H "Content-Type: application/json" --data '{"name": "TwitterTrendFlow"}' http://nifi-registry:18080/nifi-registry-api/buckets/$BUCKET_ID/flows | jq -r '.identifier')
echo "FLOW ID" $FLOW_ID

FLOW_CONF="/home/nifi/conf/registry/TwitterTrendFlow.json"

echo "Import flow"
curl -s -O /dev/null -X POST -H "Content-Type: application/json" --data @$FLOW_CONF http://nifi-registry:18080/nifi-registry-api/buckets/$BUCKET_ID/flows/$FLOW_ID/versions
curl -s -O /dev/null -X POST -H "Content-Type: application/json" --data @/home/nifi/conf/registry/TwitterTrendFlow.json http://nifi-registry:18080/nifi-registry-api/buckets/$BUCKET_ID/flows/$FLOW_ID/versions

echo "Instantiate flow"

PG="/home/nifi/conf/registry/instantiate_pg.json"
jq --arg rootid "$ROOT_ID" --arg rid "$REGISTRY_ID" --arg bid "$BUCKET_ID" --arg fid "$FLOW_ID" ' .revision.clientId |= $rootid | .component.versionControlInformation.bucketId |= $bid | .component.versionControlInformation.flowId |= $fid| .component.versionControlInformation.registryId |= $rid' $PG > $TEMP
PROCESS_GROUP_ID=$( curl -X POST -H "Content-Type: application/json" --data @$TEMP http://nifi-worker:8080/nifi-api/process-groups/$ROOT_ID/process-groups | jq -r '.id')

CTRL="/home/nifi/conf/registry/controller.json"
jq --arg  pgid "$PROCESS_GROUP_ID" ' .id |= $pgid' $CTRL > $TEMP
curl -s -O /dev/null -X PUT -H "Content-Type: application/json" --data @$TEMP http://nifi-worker:8080/nifi-api/flow/process-groups/$PROCESS_GROUP_ID/controller-services


PGStart="/home/nifi/conf/registry/process_group.json"

sleep 5
jq --arg  pgid "$PROCESS_GROUP_ID" ' .id |= $pgid' $PGStart > $TEMP
curl -X PUT -H "Content-Type: application/json" --data @$TEMP http://nifi-worker:8080/nifi-api/flow/process-groups/$PROCESS_GROUP_ID

rm $TEMP