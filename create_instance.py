#!/usr/bin/env python3
import boto3
ec2 = boto3.resource('ec2')
instance = ec2.create_instances(
    ImageId='ami-0713f98de93617bb4',
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=['sg-0990a25453de95f30'],
    KeyName='webserver_key',
    TagSpecification=[
        {
            'ResourceType': 'instance',
             'Tags': [
                 {
                     'Key': 'Name',
                     'Value': 'WebServer'
                 },
              ]
        },
    ],
    InstanceType='t2.nano')
print (instance[0].id)
