#! /usr/bin/env python3.4

#Usage: python3 ec2_start_stop.py start|stop {superset,tsdb,iot_dep_server,all}
#Example: python3 ec2_start_stop.py start superset --> this will start superset instance alone
#python3.4 ec2_start_stop.py start all --> this will start all iot instances

# Name	         : start_iot_demo.sh
# Pupose         : To start/stop IOT instances based on the given arguments
# DATE           : Tue Oct  3 10:33:18 UTC 2017
# Python Version : 3.4
# Author	 : Mahesh <mahesh@orzota.com>
# Version	 : 0.1

# Requirements   : awscli and boto3 needs to installed

import boto3
import sys
import os
import smtplib
#Variable declarations
project_name = 'cus360 cassandra'
usage = "python3.4 cassandra_ec2_start_stop.py start|stop"
instance_id = 'i-055fec6a12fec9c64'
region = "us-east-2" 
start_msg = 'starting' + ' ' + project_name + ' ' + 'instance'
stop_msg = 'stopping' + ' ' + project_name + ' ' +'instance'
user = os.environ['SUDO_USER']
TO = ['devops@orzota.com','dharmin@orzota.com','sreemathan.r@orzota.com']
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
    response = client.describe_instance_status(
        InstanceIds=[
            (ids) 
        ])  
if len(sys.argv) < 2:
    print (usage)

elif sys.argv[1] == "start":
        print (start_msg)
        start_ins(instance_id)
        send_mail(project_name + ' ' + "instance has been started by" + ' ', user)
elif sys.argv[1] == "stop":
        print (stop_msg)
        stop_ins(instance_id)
        send_mail(project_name + ' ' + "instance has been stopped by" + ' ', user)
else:
    print (usage)
