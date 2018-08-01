#! /usr/bin/env python3.4

#Usage: python3 insurance_ec2_start_stop.py start|stop|status
#Example: python3 insurance_ec2_start_stop.py start  --> this will start  instance 
# Name	         : start_iot_demo.sh
# Pupose         : To start/stop IOT instances based on the given arguments
# DATE           : Thu Dec 14 15:41:55 UTC 2017
# Python Version : 3.4
# Author	 : Mahesh <mahesh@orzota.com>
# Version	 : 2.0 
#Fixed Multiple execution bug and added status option
# Requirements   : awscli and boto3 needs to installed

import boto3
import sys
import os
import smtplib
#Variable declarations
project_name = 'Figo Demo'
usage = "python3.4 insurance_ec2_start_stop.py start|stop|status"
instance_id = 'i-0682f1c03154435b2'
region = "us-west-2" 
start_msg = 'starting' + ' ' + project_name + ' ' + 'instance'
stop_msg = 'stopping' + ' ' + project_name + ' ' +'instance'
user = os.environ['SUDO_USER']
TO = ['devops@orzota.com','anitha.m@orzota.com','aberami.g@orzota.com','sreemathan.r@orzota.com','dharmin@orzota.com','vishnu.pb@orzota.com']
def send_mail(TEXT,TEXT1):
    SUBJECT = project_name + 'Instance Start/Stop Alert'
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
    elif ins_status(instance_id) == "shutting-down" or ins_status(instance_id) == "stopped" or ins_status(instance_id) == "stopping":
        print (project_name + ' ' + "instance is in stopped state")
else:
    print (usage)
