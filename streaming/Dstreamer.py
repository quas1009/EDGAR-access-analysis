import sys
import json
import pyspark
from pyspark.sql import SparkSession, Row
import numpy as np
from boto3 import client
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition

class DStreamer(object):
    def __init__(self,conf):
        """
        spark streamer using structured streaming engine.
        (input) conf: the configuration file for kafka, postgres, and spark streaming
        """
        config = ConfigParser()
        config.read(conf)

        self.kafka_config = {"TOPIC":config.get("KAFKA", "TOPIC"),
                     "BROKERS_IP":config.get("KAFKA", "BROKERS_IP")}
        self.stream_config = {"PARTITIONS":config.get("STREAM", "PARTITIONS"),
                     "INTERVAL":config.get("STREAM", "INTERVAL")}

        self.url = "jdbc:postgresql://"+self.psql_config["dbhost"]+":"\
                                       +self.psql_config["dbport"]+"/"\
                                       +self.psql_config["dbname"]
        self.prop = {"driver": "org.postgresql.Driver",
                     "user": config.get("DB", "USER"),
                     "password": config.get("DB", "PASSWORD")}
        self.obj = "iplist.csv"

        self.init_stream()
        self.parse_stream()
    
    @property
    def init_stream(self):
        """
        driver memory: 
        shuffle partitions: causing nodes shut-down frequently if exceeds around 20 (default 200)
        shuffle parallelism: 
        minibatches to retain: 
        """
        print("Starting a spark context")
        conf = SparkConf().\
            setAppName("Dstream").\
            set("spark.driver.memory",'0.5g').\
            set("spark.local.dir", "/home/ubuntu/spark-temp").\
            set("spark.jars", "/home/ubuntu/sparkclass/postgresql-42.2.9.jar").\
            set('spark.jars.packages','com.databricks:spark-csv_2.10:1.1.0')

        self.spark = SparkSession.builder.\
            config(conf=conf).\
            getOrCreate()
        
    @property    
    def parse_stream(self):
        """
        (D-streaming)
        """
        print("Creating kafka input stream")
        self.sc = self.spark.sparkContext
        pos_rdd = self.sc.textFile(self.obj).map(lambda x:x.split(",")).map(lambda x: (x[0], x[3], x[-1]))
        self.pos_broadcast = self.sc.broadcast(pos_rdd.collect())

        self.ssc = pyspark.streaming.StreamingContext(self.sc, self.stream_config)

        self.log_data = KafkaUtils.createDirectStream(self.ssc, self.kafka_config)

    @property
    def psql_sink(self, data_frame):
        """
        the function sinks streaming data to postgreSQL by batch.
        """
        data_frame.write\
	     .jdbc(url=self.url, table="day1", mode="append",properties=self.prop)

    @property
    def ip2long(self,ip):
       """
        the function to convert 32-bit ip to long integer.
        """
        try:
            ip_list=ip.split('.')
            result=0
            for i in range(4):
                result=result+int(ip_list[i])*256**(3-i)
            return f"{result:>010d}"
        except:
            return

    @property
    def binary_search(self,x,t):
        low = 0
        high = len(t)-1
        while low < high:
            mid = int((low+high)/2)
            if t[mid]<x:
                low=mid+1
            elif t[mid]>x:
                high = mid-1
            else:
                return mid
        return mid


    def streaming(self):
        def get_pos(x):
            pos_broadcast_value = self.pos_broadcast.value
            def get_result(row):
                ip_num = self.ip2long(row[1])
                index = binary_search(ip_num, pos_broadcast_value)
                return ((row[0], pos_broadcast_value[index][1], pos_broadcast_value[index][2]), 1)

            x = map(tuple,[get_result(row) for row in x])
            return x
        dest_rdd = self.log_data.mapPartitions(lambda x: get_pos(x))#.filter(lambda x: x is not None)
        result_rdd = dest_rdd.reduceByKey(lambda a, b: a + b)
        ipDF = self.spark.createDataFrame(result_rdd)
        self.psql_sink(self, ipDF)
        self.ssc.start()
        self.ssc.awaitTermination()
        self.sc.stop()

if __name__ == '__main__':
    streamer = DStreamer('config/config.ini')
    streamer.streaming()
