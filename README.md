# **Animaly Detection**
This project is a simple anomaly detection application. I set up a streaming pipeline with spark and kafka through docker containers. 

## Docker-Compose File
This docker-compose includes 7 services that communicate with each other through a network called kafka-spark. the services are:

1- Zookeeper         172.18.0.8

2- kafka             172.18.0.9

3- spark (master)    172.18.0.10

4- spark-worker-1    172.18.0.11

5- spark-worker-2    172.18.0.12

6- anomaly_detection 172.18.0.13

7- producer          172.18.0.14


## Running services
### **clone the repository**
```
git clone https://github.com/ShadiDastgerdi/anomaly-detection.git
cd anomaly-detection
```

### **create jars_dir directory**
Create a directory called jars_file. anomaly-detection jar files will be stored in this directory.
```
sudo mkdir jars_dir
sudo chown -R root:root jars_dir
sudo chmod -R 775 jars_dir
```
### **change the permissions on files and directory**
To save anomaly_detection.py checkpoints in the code directory, change the permissions on this direcory:
```
sudo chown -R root:root code
sudo chmod -R 775 code
```
To run the scripts, change the following permissions:
```
sudo chmod +x kafka_script/producer.sh
sudo chmod +x code/consumer.sh
```
### **Run docker-compose.yml**
```
docker-compose up
```
