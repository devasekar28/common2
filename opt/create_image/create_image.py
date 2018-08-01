#!/usr/bin/env python3.4
import boto3
import sys
from datetime import datetime
now = datetime.now()
today_date = (str(now.month) + "-" + str(now.day) + "-" + str(now.year) + " " + str(now.hour) + str(now.minute) + str(now.second))
ami_name = ("Mahesh_RND_" + today_date)
def create_image(id):
    client = boto3.client('ec2', region_name='us-east-2')
    response = client.create_image(
        Description=ami_name,
        InstanceId=id,
        Name=ami_name,
        NoReboot=True
    )
    return  (response['ImageId'])


def terminate_instance(id):
    client = boto3.client('ec2', region_name='us-east-2')
    response = client.terminate_instances(
        InstanceIds=[
            (id)
        ])

if len(sys.argv) < 2:
    print ("usage: python3 create_image.py image_id")
else:
    ec2 = boto3.resource('ec2', region_name='us-east-2')
    ami_id = create_image(sys.argv[1])
    print (ami_id)
    image = ec2.Image(ami_id)
    print ("waiting for image state to be available")
    image.wait_until_exists(
        Filters=[
            {
                'Name': 'state',
                'Values': [
                    'available',
                ]
            }
        ]
    )
    print (sys.argv[1] + "Image has been created")
    print ("terminating instance")
    terminate_instance(sys.argv[1]) 
