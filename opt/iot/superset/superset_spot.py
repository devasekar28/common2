#! /usr/bin/env python3.4

#Usage: sudo /bin/python3.4 /opt/iot_client/iotclient_spot.py  price|create{price}|terminate|status
#To get current prices in all availability regions: sudo /bin/python3.4 /opt/iot_client/iotclient_spot.py  price
#To create instance with spot price sudo /bin/python3.4 /opt/iot_client/iotclient_spot.py create 0.003
# Name           : /opt/iot_client/iotclient_spot.py 
# Pupose         : To create/terminate IOT Client instances based on the given arguments
# DATE           : Wed Jan 17 09:49:33 UTC 2018
# Python Version : 3.4
# Author         : Mahesh <mahesh@orzota.com>
# Version        : 3.0 Added spot price declaration in this release
# Requirements   : awscli and boto3 needs to installed

import boto3
import sys
import os
import smtplib
import datetime
import tzlocal
from collections import defaultdict

user = os.environ['SUDO_USER']
#TO = ['mahesh@orzota.com']
TO = ['devops@orzota.com','karthigeyan@orzota.com,','vishnu.pb@orzota.com','anitha.m@orzota.com','aberami.g@orzota.com','sreemathan.r@orzota.com','venkata@orzota.com','saiteja.mv@orzota.com']
#Function to send E-mail alert to the users
def send_mail(TEXT,TEXT1):
    SUBJECT = 'Orzota IOT-Client Spot Instance Create/Terminate Alert'
    #TEXT = serv + ' ' + "IOT instance has been started by", user
    TEXT = TEXT + TEXT1
    #print (TEXT)
    #print (' '.join(TEXT))
    # Gmail Sign In
    gmail_sender = 'orzota.customer1@gmail.com'
    gmail_passwd = 'Customer1!'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)
    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])
    #print (BODY)
    try:
        server.sendmail(gmail_sender, TO, BODY)
        #print ('email sent')
    except:
        print ('error sending mail')

    server.quit()

#Function to get instance detail using Name tag
def instance_details(tagkey, tag_value):

    ec2 = boto3.resource('ec2', region_name='us-east-2')
    
    # Get information for all running instances
    running_instances = ec2.instances.filter(Filters=[{
        'Name': tagkey,
        'Values': [tag_value]}])
    
    ec2info = defaultdict()
    for instance in running_instances:
        for tag in instance.tags:
            if 'Name'in tag['Key']:
                name = tag['Value']
        # Add instance info to a dictionary         
        ec2info[instance.id] = {
            'Name': name,
            'Type': instance.instance_type,
            'State': instance.state['Name'],
            'Private IP': instance.private_ip_address,
            'Public IP': instance.public_ip_address,
            'Launch Time': instance.launch_time,
            'Keypair': instance.key_name
            }
    
    attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time','Keypair']
    for instance_id, instance in ec2info.items():
        for key in attributes:
            print("{0}: {1}".format(key, instance[key]))
        print("------")

#Main function to create spot instance with image_id, image_type, spot_price, instance_name(tag Name)    
def create_spot(image_id, image_type, spot_price, instance_name):
    client = boto3.client('ec2', region_name='us-east-2')
    response = client.request_spot_instances(
        DryRun=False,
        SpotPrice=spot_price,
        InstanceCount=1,
        Type='one-time',
        LaunchSpecification={
            'ImageId': image_id,
            'KeyName': 'Accesskeypair',
            'Placement':{},
            'SubnetId': 'subnet-66614f2c',
            'InstanceType': image_type,
            'BlockDeviceMappings': [
                {  
                    'DeviceName': '/dev/sda1', 
                    'Ebs': {
                        'VolumeSize': 30,
                        'DeleteOnTermination': True,
                        'VolumeType': 'gp2',
                    },
                },
            ],
    
            'EbsOptimized': True,
            'Monitoring': {
                'Enabled': False
            },
            'SecurityGroupIds': [
                'sg-9917e1f0',
            ],
        }
    )
    
    va = response['SpotInstanceRequests']
    spot_id = va[0]['SpotInstanceRequestId']
    #print (spot_id)
    waiter = client.get_waiter('spot_instance_request_fulfilled')
    print("waiting until spot instance will available")
    waiter.wait(SpotInstanceRequestIds=[spot_id])
    print("spot instance request fullfilled")
    #Getting instance id
    instance_id = client.describe_spot_instance_requests(
                SpotInstanceRequestIds=[
                  spot_id,
                ],
    )['SpotInstanceRequests'][0]['InstanceId']
    client.create_tags(Resources=[instance_id], Tags=[{'Key':'Name', 'Value': instance_name}])
    #Writing instance id to the temporary file. This file content will be used while terminating instance
    instance_file = open('instance_id.txt', 'w')
    instance_file.write(instance_id)
    #print(instance_id)
    return instance_id

#This function is used to terminate the instance 
def terminate_spot(ids):
    client = boto3.client('ec2', region_name='us-east-2')
    response = client.terminate_instances(
    InstanceIds=[
        ids,
    ])    

def spot_price():
    client = boto3.client('ec2', region_name='us-east-2')
    regions = [x["RegionName"] for x in client.describe_regions()["Regions"]]
    INSTANCE = "m4.large"
    print("Instance: %s" % INSTANCE)
    results = []
    for region in regions:
        client = boto3.client('ec2', region_name="us-east-2")
        prices = client.describe_spot_price_history(
            InstanceTypes=["m4.large"],
            ProductDescriptions=['Linux/UNIX', 'Linux/UNIX (Amazon VPC)'],
            StartTime=(datetime.datetime.now() -
                       datetime.timedelta(hours=4)).isoformat(),
            #Filters=[{'Name': 'availability-zone', 'Values': zones}],
        )
        for price in prices["SpotPriceHistory"]:
            #print (price)
            results.append((price["AvailabilityZone"], price["SpotPrice"]))
    #print (results)    
    for region, price in sorted(set(results), key=lambda x: x[1]):
        print("Region: %s price: %s" % (region, price))
try:
    price=sys.argv[2]
except:
    pass

if len(sys.argv) < 2:
    print ("usage: sudo python3.4 /opt/iot_client/iotclient_spot.py price|create {price}|terminate|status")
elif sys.argv[1] == "create":
    try:
        print('Creating IOT Client Spot Instance')
        #Calling Function create_spot with Arguments
        create_spot('ami-27e0ca42', 'm4.large', price, 'IOT_Client')
        #print(price)
        #Calling Function instance_details to get all details about launched spot instance
        instance_details('tag:Name','IOT_Client')
        send_mail("IOT-Client Spot instance has been created by" + ' ', user)
    except NameError as err:
        print (err, "Proceed with price value")
        print ("To get current spot price execute this: sudo python3.4 /opt/iot_client/iotclient_spot.py price")
        print ("Example: sudo python3.4 /opt/iot_client/iotclient_spot.py create {spot price}")
elif sys.argv[1] == "terminate":
    try:
        #Reading instance id from temporary file
        var = open("instance_id.txt", "r+") 
        instance_id = var.read()
        print('Terminating IOT Client Spot Instance')
        #terminating instnce
        print(instance_id)
        terminate_spot(instance_id)
        var.close()
        #Removing Temporary file
        os.remove("instance_id.txt") 
        send_mail("IOT-Client Spot instance has been terminated by" + ' ', user)
    except FileNotFoundError as err:
        print("Currently there is no running iot client instance")
        print("To create instance: sudo python3.4 /opt/iot_client/iotclient_spot.py create {spot price}")
 
elif sys.argv[1] == "status":
    if os.path.exists('instance_id.txt')==True:
        print ("Iot client instance is in running state:") 
        instance_details('tag:Name','IOT_Client')
    elif os.path.exists('instance_id.txt')==False:
        print ("Currently there is no running iot_client instance")

elif sys.argv[1] == "price":
    spot_price() 
else:
    print ("usage: sudo python3.4 /opt/iot_client/iotclient_spot.py price|create {price}|terminate|status")
