#! /usr/bin/env python3.4

#Usage: python 3.4 /opt/oregon_cdh/start_stop.py {start|stop}
#Example: python3.4 /opt/oregon_cdh/start_stop.py start

# Name	         : /opt/oregon_cdh/start_stop.py
# Pupose         : To start/stop oregon CDH cluster instances
# DATE           : Tue Oct  3 10:33:18 UTC 2017
# Python Version : 3.4
# Author	 : Mahesh <mahesh@orzota.com>
# Version	 : 0.1
# Requirements   : awscli and boto3 needs to installed

import boto3
import sys
import os 
import smtplib
clouderamanager = 'i-0d7520c4df32c4309'
namenode = 'i-0492c5ccccdb9d0cf'
datanode1 = 'i-09649d17d11032a29'
datanode2 = 'i-09caa411b31d09bc5'
accessnode = 'i-073fe598f4a7812ff'
ins_list = [clouderamanager,namenode,datanode1,datanode2,accessnode]
user = os.environ['SUDO_USER']
TO = ['devops@orzota.com','karthigeyan@orzota.com','siddesh@orzota.com','venkata@orzota.com','aberami.g@orzota.com','anitha.m@orzota.com','vishnu.pb@orzota.com']
#TO = ['mahesh@orzota.com','deva@orzota.com']
def send_mail(TEXT,TEXT1):
    SUBJECT = 'Oregon CDH Cluster Start/Stop Alert'
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
    client = boto3.client('ec2', region_name='us-west-2')
    response = client.start_instances(
        InstanceIds=[
            (ids)
        ])

def stop_ins(ids):
    client = boto3.client('ec2', region_name='us-west-2')
    response = client.stop_instances(
        InstanceIds=[
            (ids)
        ])

def ins_status(ids):
    client = boto3.client('ec2', region_name='us-west-2') 
    response = client.describe_instance_status(
        InstanceIds=[
            (ids) 
        ])  

def ins_pub_ip(id):
    ec2 = boto3.resource('ec2', region_name='us-west-2')
    instance = ec2.Instance(id)
    return instance.public_ip_address

    
if len(sys.argv) < 2:
    print("usage: python3.4 /opt/oregon_cdh/start_stop.py {start|stop} ")
elif sys.argv[1] == "start":    
    print ("Starting Oregon CDH cluster instances")
    for instance in ins_list:
        start_ins(instance)
    send_mail("Oregon CDH instances has been started by" + ' ', user)
    print ("Clouderamanger URL:" + ' ',"http://" + ins_pub_ip(clouderamanager) + ":7180")
    print ("Please start ALL the services using cloudera manager")
    print ("Access node IP is: " + ' ', ins_pub_ip(accessnode))
    print ("Please do SSH login with ldap credentials in access node")

elif sys.argv[1] == "stop":
    print ("Stopping Oregon CDH cluster instances")
    for instance in ins_list:
        stop_ins(instance)
    send_mail("Oregon CDH instances has been stopped by" + ' ', user)

else:
    print("usage: python3.4 /opt/oregon_cdh/start_stop.py {start|stop} ")


