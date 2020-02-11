from __future__ import print_function
import sys
import time
import json
from boto3 import client
import lazyreader
from configparser import ConfigParser
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient

class KProducer(object):
    """
    ingest data from S3 to Kafka
    """
    def __init__(object):
        """
        initialize instances of AWS-S3 and Kafka
        """
        config = ConfigParser()
        config.read(object)

        self.aws_config   = {"aws_access_key_id": config.get("AWS", "ACCESS"),
                             "aws_secret_access_key": config.get("AWS", "SECRET")}
        self.s3_config    = {"BUCKET":config.get("S3", "BUCKET"),
                             "KEY":config.get("S3", "KEY")}
        self.kafka_config = {"TOPIC":config.get("KAFKA", "TOPIC"),
                             "BROKERS_IP":config.get("KAFKA", "BROKERS_IP")}
        self.producer = KafkaProducer(bootstrap_servers=[self.kafka_config["BROKERS_IP"]])
    
    
    def send_message(self):
        """
        send messages to Kafka topic
        """
        while True:
            s3 = client('s3', self.aws_config)
            obj = s3.get_object(Bucket=self.s3_config["BUCKET"], Key=self.s3_config["KEY"])
            for line in lazyreader.lazyread(obj["Body"], delimiter=b'\n'):
                value1 = line.decode().split(',')
                json_data = json.dumps({'ip': value1[0][:-3]+'0',  # mask ip: a.b.c.x -> a.b.c.0
                                        'date': value1[1],
                                        'time': value1[2],
                                        'cik': value1[4][:-2],
                                        'code': value1[7]}).encode('utf-8')
                self.producer.send(topic = self.kafka_config["TOPIC"], value=json_data)
                time.sleep(0.01)       # avoid disk overload


if __name__ == '__main__':    
    args = sys.argv
    partition_key = str(args[1])
    CONFIGPATH = "config/config.ini"
    prod = KProducer(CONFIGPATH)
    prod.send_message()