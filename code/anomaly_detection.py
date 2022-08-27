from pyspark.sql import SparkSession
from pyspark.sql.streaming import *
from pyspark.sql.functions import from_unixtime, col, window, when, split
from pyspark.sql.types import StructType

def parse_data_from_kafka_message(sdf, schema):
    assert sdf.isStreaming == True, "DataFrame doesn't receive streaming data"
    col = split(sdf['value'], ',') 
    for idx, field in enumerate(schema): 
        sdf = sdf.withColumn(field.name, col.getItem(idx).cast(field.dataType))
    return sdf.select([field.name for field in schema])
  
def check_anomaly(mean, sd):
    userSchema = StructType().add("time", "float").add("cpu", "float")
    streamdata = parse_data_from_kafka_message(df, userSchema)
    df3=streamdata.select(from_unixtime(col("time")/1000).alias("time"),col("cpu")) 
    query = df3.groupBy(window(col("time"), "0.1 second")).mean("cpu")
    query = query.withColumn("status", \
                         when(((col("avg(cpu)") > mean) & (col("avg(cpu)") > mean + 2*sd)) | ((col("avg(cpu)") < mean) & (col("avg(cpu)") < mean - 2*sd)) , "Error")\
                         .when(((col("avg(cpu)") > mean) & (col("avg(cpu)") > mean + sd)) | ((col("avg(cpu)") < mean) & (col("avg(cpu)") < mean - sd)), "Warning")\
                         .otherwise("OK"))
    query = query.filter(col("status") != "OK") 
    return query

if __name__ == "__main__":

    spark = SparkSession \
    .builder \
    .appName("Spark Kafka Streaming") \
    .master("spark://172.18.0.10:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

    MEAN = 14.94
    STANDARD_DEV1 = 3.35
 
    spark.sparkContext.setLogLevel("ERROR")
    df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "172.18.0.9:9093") \
    .option("subscribe", "cpu_time") \
    .option("startingOffsets", "earliest") \
    .option("includeHeaders", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

    query = check_anomaly(MEAN, STANDARD_DEV1)
    query.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("checkpointLocation", "/opt/bitnami/spark/ivy/code/checkpoint")\
    .option("truncate", False) \
    .start() \
    .awaitTermination()
