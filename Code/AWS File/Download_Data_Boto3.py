import os
import ssl
import logging
import boto3
from botocore.exceptions import ClientError
import pandas as pd
import configparser

cwd = os.path.dirname(os.path.realpath(__file__))
FilePath = cwd + '\\aws.config'

config = configparser.ConfigParser()
config.read(FilePath)

Access_key_ID = config.get('AWS_Credentials', 'Access_key_ID')
Secret_access_key = config.get('AWS_Credentials', 'Secret_access_key')
Region_Name = config.get('AWS_Credentials', 'Region_Name')

start_byte = 0
stop_byte=1000000

client = boto3.client(
    's3',
    aws_access_key_id=Access_key_ID,
    aws_secret_access_key=Secret_access_key,
    region_name=Region_Name
)
Objects = client.get_object(Bucket='rippled-fullhistory', Key='08232019/transaction.db', Range='bytes={}-{}'.format(start_byte, stop_byte))
# Objects = client.get_object(Bucket='rippled-fullhistory', Key='08232019/transaction.db')
content = Objects['Body']
X1 = content.read()

with open('Temp.db', 'wb') as w:
    w.write(X1)

X1