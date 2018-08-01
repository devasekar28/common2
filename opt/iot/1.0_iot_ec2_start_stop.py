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
superset = 'i-0287b0a434bea4faf'
tsdb = 'i-02d75441f0f86fcca'
iot_dep_server = 'i-0ea1d52d0b3aba9d6'
user = os.environ['SUDO_USER']
TO = ['devops@orzota.com','karthigeyan@orzota.com,','vishnu.pb@orzota.com','anitha.m@orzota.com','aberami.g@orzota.com','sreemathan.r@orzota.com','venkata@orzota.com','saiteja.mv@orzota.com']
def send_mail(TEXT,TEXT1):
    SUBJECT = 'Orzota IOT Instance Start/Stop Alert'
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
    client = boto3.client('ec2')
    response = client.start_instances(
        InstanceIds=[
            (ids)
        ])

def stop_ins(ids):
    client = boto3.client('ec2')
    response = client.stop_instances(
        InstanceIds=[
            (ids)
        ])

def ins_status(ids):
    client = boto3.client('ec2') 
    response = client.describe_instance_status(
        InstanceIds=[
            (ids) 
        ])  
ins_list=[superset,tsdb,iot_dep_server]
#print (ins_list)
if len(sys.argv) < 3:
    print ("python3.4 ec2_start_stop.py start|stop {superset,tsdb,iot_dep_server,all}")

elif sys.argv[1] == "start":
    if sys.argv[2] == "superset":
        print ("starting superset instance")
        start_ins(superset)
        send_mail("superset" + ' ' + "IOT instance has been started by" + ' ', user)
    elif sys.argv[2] == "tsdb":
        print ("starting timescale db instance")
        start_ins(tsdb)
        send_mail("tsdb" + ' ' + "IOT instance has been started by" + ' ', user)
    elif sys.argv[2] == "iot_dep_server":
        print ("starting IOT Deployment server")
        start_ins(iot_dep_server)
        send_mail("iot_dep_server" + ' ' + "IOT instance has been started by" + ' ', user )
    elif sys.argv[2] == "all":
        print ("Starting All IOT instances")
        for instance in ins_list:
            start_ins(instance)
        send_mail("All" + ' ' + "IOT instance has been started by" + ' ', user)
    else:
        print ("python3.4 ec2_start_stop.py start|stop {superset,tsdb,iot_dep_server,all")

elif sys.argv[1] == "stop":
    if sys.argv[2] == "superset":
        print ("stopping superset instance")
        stop_ins(superset)
        send_mail("superset" + ' ' + "IOT instance has been stopped by" + ' ', user)
    elif sys.argv[2] == "tsdb":
        print  ("stopping tsdb instance")
        stop_ins(tsdb)
        send_mail("tsdb" + ' ' + "IOT instance has been stopped by" + ' ', user)
    elif sys.argv[2] == "iot_dep_server":
        print ("stopping IOT deployment server")
        stop_ins(iot_dep_server)
        send_mail("iot_dep_server" + ' ' + "IOT instance has been stopped by" + ' ', user)
    elif sys.argv[2] == "all":
        print ("Stopping all IOT instances")
        for instance in ins_list:
            stop_ins(instance)    
        send_mail("All" + ' ' + "IOT instance has been stopped by" + ' ', user)
    else:
        print ("python3.4 ec2_start_stop.py start|stop {superset,tsdb,iot_dep_server,all}")


else:
    print ("python3.4 ec2_start_stop.py start|stop {superset,tsdb,iot_dep_server,all}")
