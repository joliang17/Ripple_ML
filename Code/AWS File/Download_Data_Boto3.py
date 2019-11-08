import ssl
import logging
import boto3
from botocore.exceptions import ClientError
import pandas as pd
# from ConfigParser import SafeConfigParser

# parser = SafeConfigParser()
# parser.read('aws.config')

# Access_key_ID = parser.get('bug_tracker', 'Access_key_ID')
# Secret_access_key = parser.get('bug_tracker', 'Secret_access_key')
# Region_Name = parser.get('bug_tracker', 'Region_Name')

start_byte = 0
stop_byte=1000000

client = boto3.client(
    's3',
    aws_access_key_id='AKIAYPDHIEPY4PWX72LR',
    aws_secret_access_key='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',
    region_name='us-west-2'
)
Objects = client.get_object(Bucket='rippled-fullhistory', Key='08232019/transaction.db', Range='bytes={}-{}'.format(start_byte, stop_byte))
# Objects = client.get_object(Bucket='rippled-fullhistory', Key='08232019/transaction.db')
content = Objects['Body']
X1 = content.read()

with open('Temp.db', 'wb') as w:
    w.write(X1)

X1
# response = s3.list_buckets()

# print('Existing buckets:')
# for bucket in response['Buckets']:
#     print(f'  {bucket["Name"]}')
