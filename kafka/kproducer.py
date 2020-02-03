from __future__ import print_function
import time
import json
import argparse
from boto3 import client
import lazyreader
import sys
from kafka import KafkaProducer
from configparser import ConfigParser
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from time import sleep

def send_message(producer, obj):
    for line in lazyreader.lazyread(obj['Body'], delimiter=b'\n'):
        value1 = line.decode().split(',')
        json_data = json.dumps({'ip': value1[0][:-3]+'0',
                                'date': value1[1],
                                'time': value1[2],
                                'cik': value1[4],
                                'doc': value1[5],
                                'ext': value1[6],
                                'code': value1[7],
                                'crawl': value1[12],
                                'bro': value1[13]}).encode('utf-8')
        producer.send(topic = 'test', value=json_data)



if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-rh', '--host', default="ip-10-0-0-5:9092,ip-10-0-0-4:9092,ip-10-0-0-14:9092")
#     parser.add_argument('-t', '--topic', default='test')
#     parser.add_argument('-i', '--input', required=True)
#     args = parser.parse_args()
    
    args = sys.argv
    partition_key = str(args[1])
    
    # config S3
    config = ConfigParser()
    config.read('config.ini')
    aws_access = {
        'aws_access_key_id': config.get('AWS Access', 'access_key'),
        'aws_secret_access_key': config.get('AWS Access', 'secret_key')
    }
    s3 = client('s3', **aws_access)
    obj = s3.get_object(Bucket='jywang', Key='log20170101.csv')
        
    # create kafka topics
#     print(f"Create Kafka topics: {args.topic}")
#     admin_client = KafkaAdminClient(bootstrap_servers=args.host, client_id='test')
#     topic_list = []
#     topic_list.append(NewTopic(name=args.topic, num_partitions=6, replication_factor=3))
#     try:
#         admin_client.create_topics(new_topics=topic_list, validate_only=False)
#     except TopicAlreadyExistsError as err:
#         print("topics already exisit...")
    # push data to kafka
#     print(f"Pushing data to Kafka topic: {topic}")
    producer = KafkaProducer(bootstrap_servers=['ip-10-0-0-11:9092','ip-10-0-0-14:9092','ip-10-0-0-7:9092','ip-10-0-0-8:9092'])#,
    send_message(producer, obj)
    time.sleep(0.01)