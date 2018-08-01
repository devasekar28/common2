#! /usr/bin/env python3.4
#Usage: python3 iot_demo_aqmd_start_stop.py start|stop|status
#Example: python3 iot_demo_aqmd_start_stop.py start  --> this will start instance 

# Name	         : start_iot_demo.sh
# Pupose         : To start/stop IOT instances based on the given arguments
# DATE           : Fri Jan  5 09:24:41 UTC 2018
# Python Version : 3.4
# Author	 : Mahesh <mahesh@orzota.com>
# Version	 : 0.1
# Requirements   : awscli and boto3 needs to installed

import boto3
import sys
import os
import smtplib
from collections import defaultdict

#Variable declarations
project_name = 'iot_demo_aqmd'
usage = "sudo python3.4 iot_demo_aqmd_start_stop.py start|stop|status"
instance_id = 'i-0944e284da9653602'
region = "us-west-2" 
start_msg = 'starting' + ' ' + project_name + ' ' + 'instance'
stop_msg = 'stopping' + ' ' + project_name + ' ' +'instance'
user = os.environ['SUDO_USER']
TO = ['devops@orzota.com','karthigeyan@orzota.com,','vishnu.pb@orzota.com','anitha.m@orzota.com','aberami.g@orzota.com','sreemathan.r@orzota.com','venkata@orzota.com']
def send_mail(TEXT,TEXT1):
    SUBJECT = project_name + ' Instance Start/Stop Alert'
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

def instance_details(tagkey, tag_value):

    ec2 = boto3.resource('ec2', region_name='us-west-2')

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


def start_ins(ids):
    client = boto3.client('ec2', region_name=region)
    response = client.start_instances(
        InstanceIds=[
            (ids)
        ])

def stop_ins(ids):
    client = boto3.client('ec2', region_name=region)
    response = client.stop_instances(
        InstanceIds=[
            (ids)
        ])

def ins_status(ids):
    client = boto3.client('ec2', region_name=region)
    response = client.describe_instances(
            InstanceIds=[
                ids,
            ])['Reservations'][0]['Instances'][0]['State']['Name']
    return response


if len(sys.argv) < 2:
    print (usage)

elif sys.argv[1] == "start":
    if ins_status(instance_id) == "running" or ins_status(instance_id) == "pending":
        print (project_name + ' ' +"instance is already in running state please check mail about who has started")
    elif ins_status(instance_id) == "shutting-down" or ins_status(instance_id) == "stopping":
        print (project_name + ' ' +"instance is in stopping state. Please wait untill it stopped")
    else:
        print (start_msg)
        start_ins(instance_id)
        send_mail(project_name + ' ' + "instance has been started by" + ' ', user)
elif sys.argv[1] == "stop":
    if ins_status(instance_id) == "shutting-down" or ins_status(instance_id) == "stopped" or ins_status(instance_id) == "stopping":
        print (project_name + ' ' + "instance is already in stopped state. Please check mail about who has started")
    else:
        print (stop_msg)
        stop_ins(instance_id)
        send_mail(project_name + ' ' + "instance has been stopped by" + ' ', user)
elif sys.argv[1] == "status":
    if ins_status(instance_id) == "running" or ins_status(instance_id) == "pending":
        print (project_name + ' ' + "instance is running")
        instance_details('tag:Name','AQMD_IOT_DEMO')
    elif ins_status(instance_id) == "shutting-down" or ins_status(instance_id) == "stopped" or ins_status(instance_id) == "stopping":
        print (project_name + ' ' + "instance is in stopped state")
else:
    print (usage)

