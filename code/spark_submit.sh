#!/bin/bash

# create topic if not exists

spark-submit --packages 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0' --master 'spark://172.18.0.10:7077' --class Streaming --conf spark.jars.ivy=/opt/bitnami/spark/ivy /opt/bitnami/spark/ivy/code/anomaly_detection.py




