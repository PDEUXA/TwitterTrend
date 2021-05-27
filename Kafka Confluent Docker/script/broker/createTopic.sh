#!/bin/bash

kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic twitter --config retention.ms=25200000
