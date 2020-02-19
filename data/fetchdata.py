#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import date as datetime_date
from datetime import timedelta
from os import system
from os.path import abspath
from configparser import ConfigParser
from multiprocessing import Process

from boto3 import client

def fetch(aws, line):
    """Download Log File and Save"""
    zipname = os.path.split(line)[1] 
    name = zipname.split('.')[0]
    csvname = name + '.csv'
    system('rm {}'.format(csvname))
    system('wget {}'.format(line))
    system('unzip {} {}'.format(zipname, csvname))
    system('rm {}'.format(zipname))
    aws.upload_file(Filename=csvname, 
                    Bucket='jywang', Key=csvname)
    system('rm {}'.format(csvname))

if __name__ == "__main__":
    config = ConfigParser()
    config.read(abspath('config.ini'))
    aws_access = {
        'aws_access_key_id': config.get('AWS Access', 'access_key'),
        'aws_secret_access_key': config.get('AWS Access', 'secret_key')
    }
    s3 = client('s3', **aws_access)

    f= open("edgarLOGS.txt","r")
    i = 0
    for line in f:
        Process(target=fetch, args=(s3, line)).start()