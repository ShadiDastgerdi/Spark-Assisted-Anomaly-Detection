#!/bin/bash

# create topic if not exists
kafka-topics.sh --create --if-not-exists --topic cpu_time --partitions 1 --replication-factor 1 -bootstrap-server kafka:9093

filename='/opt/bitnami/kafka_data/cpu_usage.data'
n=1
while read line; do
# reading each line
echo "Line No. $n : $line"
echo "*************"
# send 
echo "$line" | kafka-console-producer.sh --broker-list kafka:9093 --topic cpu_time
n=$((n+1))
sleep 5
done < $filename




