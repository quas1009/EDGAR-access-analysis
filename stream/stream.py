from __future__ import print_function
import sys
import os
from pyspark.sql import SparkSession
from pyspark import SparkConf
import time
from pyspark.sql import functions as F
from pyspark.sql import types as T
from configparser import ConfigParser
import time
from datetime import datetime
import json
from pyspark.sql.functions import udf
import pyspark.sql.functions as f
from pyspark.sql.types import *
import pickle
from pyspark.sql.functions import expr

class Streamer(object):
    def __init__(self):
        """
    
        """
        config = ConfigParser()
        config.read(object)

        self.kafka_config = {"TOPIC":config.get("KAFKA", "TOPIC"),
                     "BROKERS_IP":config.get("KAFKA", "BROKERS_IP")}

        self.url = "jdbc:postgresql://"+self.psql_config["dbhost"]+":"\
                                       +self.psql_config["dbport"]+"/"\
                                       +self.psql_config["dbname"]
        self.prop = {"driver": "org.postgresql.Driver",
                     "user": config.get("DB", "USER"),
                     "password": config.get("DB", "PASSWORD")}

        self.schema = T.StructType().\
            add("ip", T.StringType()).\
            add("date", T.StringType()).\
            add("time", T.StringType()).\
            add("cik", T.StringType()).\
            add("code", T.StringType()) 


    def init_stream(self):
        """
        driver memory: 
        shuffle partitions: causing nodes shut-down frequently if exceeds around 20 (default 200)
        shuffle parallelism: 
        minibatches to retain: 
        """
        print("Starting a spark context")
        conf = SparkConf().\
            setAppName("stream").\
            set("spark.driver.memory",'0.5g').\
            set("spark.local.dir", "/home/ubuntu/spark-temp").\
            set("spark.jars", "/home/ubuntu/sparkclass/postgresql-42.2.9.jar").\
            set('spark.jars.packages','com.databricks:spark-csv_2.10:1.1.0').\
            set("spark.sql.shuffle.partitions", "4").\
            set("spark.default.parallelism", "4").\
            set("spark.sql.streaming.miniBatchesToRetain", "2")

        self.spark = SparkSession.builder.\
            config(conf=conf).\
            getOrCreate()

        
    def parse_stream(self):
        """
        offset: default offset (structured streaming)
        """
        print("Creating kafka input stream")
        raw_df = (self.spark.readStream.\
            format("kafka").\
            option("kafka.bootstrap.servers",self.kafka_config["BROKERS_IP"]).\
            option("subscribe", self.kafka_config["TOPIC"]).\
            load()
    
        logs_json_df = raw_df
          .selectExpr("CAST(value AS STRING)")
          .select(F.from_json("value", self.schema).alias("data"))

        logs_df = (logs_json_df
          .select(F.col("data.ip").alias("ip"),
                  F.col("data.date").alias("date"),
                  F.col("data.cik").alias("cik"),
                  F.to_timestamp(F.col("data.time"), "HH:mm:ss").alias("time"),
                  F.col("data.code").cast("int").alias("code"))
        )

    def psql_sink(data_frame, batch_id):
        data_frame.write\
	     .option("numPartitions",1)\
	     .jdbc(url=self.url, table="day1", mode="append",properties=self.prop)

    def ip2long(self,ip):
        try:
            ip_list=ip.split('.')
            result=0
            for i in range(4):
                result=result+int(ip_list[i])*256**(3-i)
            return f"{result:>010d}"
        except:
            return
    
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
        
    def join(self):
        # define udf function
        file = open('iplist', 'rb')
        iplist = pickle.load(file)
        file.close()

        def get_pos(x):
            ip_num = ip2long(x)
            index = binary_search(ip_num, iplist)
            return index
        pos_udf=udf(get_pos,StringType())

        # Load static dataframe
        df_bank = (spark.read.format("csv")
            .option("header", "true")
            .load("bank.csv"))
        # df_bank.withColumn("cik",df_bank["cik"].cast(StringType()))
                        
        logs_wm_df = (self.logs_df.withWatermark("time", "1 seconds")
                      .join(df_bank,"cik","left")
                      .groupBy(F.col("ip"),F.col("cik"), F.window(F.col("time"), "1 seconds", "1 seconds"))
                      .agg(F.count("code").alias("req_count"))
                      .select(F.col("ip"), F.col("cik"), F.col("window.start").alias("start"), F.col("req_count"), pos_udf(F.col("ip")).alias("region"))
                     )


#     logs_watermarked_df = (logs_df
#       .withWatermark("time", "20 seconds")
#       .groupBy(F.col("ip"),
#                F.window(F.col("time"), "20 seconds", "10 seconds"))
#       .agg(F.count('code').alias('req_count'),
#            F.count('crawl').alias('cra_count'))
#       .select(F.col("ip").alias("suspicious_ip")))
#    suspicious_ip_df = logs_wm_df.filter("req_count > 1000")
    
        print("Start Streaming")
        file_output_stream = (logs_wm_df
          .writeStream
          .foreachBatch(self.psql_sink)
          .outputMode("update")      
               .trigger(processingTime='5 seconds')
          .queryName("file_output_stream")
          .start().awaitTermination())  


if __name__ == '__main__':
    streamer = Streamer('config/config.ini')
