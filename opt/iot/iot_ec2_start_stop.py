#! /usr/bin/env python3.4

#Usage: python3 ec2_start_stop.py start|stop|status {superset,tsdb,iot_dep_server,all}
#Example: python3 ec2_start_stop.py start superset --> this will start superset instance alone
#python3.4 ec2_start_stop.py start all --> this will start all iot instances

# Name	         : start_iot_demo.sh
# Pupose         : To start/stop IOT instances based on the given arguments
# DATE           : Fri Dec 15 04:56:52 UTC 2017
# Python Version : 3.4
# Author	 : Mahesh <mahesh@orzota.com>
# Version	 : 2.0
# Fixed mulitple execution of start/stop issue And added status optio
# Requirements   : awscli and boto3 needs to installed

import boto3
import sys
import os
import smtplib
instance_dict = {'superset':'i-0287b0a434bea4faf','tsdb':'i-02d75441f0f86fcca', 'iot_dep_server':'i-05cd248ee51bf69e5'}
region = "us-east-1"
user = os.environ['SUDO_USER']
#TO = ['deva@orzota.com']
TO = ['devops@orzota.com','karthigeyan@orzota.com,','vishnu.pb@orzota.com','anitha.m@orzota.com','aberami.g@orzota.com','sreemathan.r@orzota.com','venkata@orzota.com','saiteja.mv@orzota.com','prachi@orzota.com']
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

if len(sys.argv) < 3:
    print ("python3.4 ec2_start_stop.py start|stop|status {superset,tsdb,iot_dep_server,all}")

elif sys.argv[1] == "start":
    if sys.argv[2] == "superset":
        if ins_status(instance_dict['superset']) == "running" or ins_status(instance_dict['superset']) == "pending":
            print("Superset instance already in running state and please check mail about who has started")
        else:
            print ("starting 34.231.254.23 superset instance")
            start_ins(instance_dict['superset'])
            send_mail("superset" + ' ' + "34.231.254.23 IOT instance has been started by" + ' ', user)
    elif sys.argv[2] == "tsdb":
        if ins_status(instance_dict['tsdb']) == "running" or ins_status(instance_dict['tsdb']) == "pending":
            print("TSDB instance is already in running state and please check mail about who has started")
        else:
            print ("starting 34.196.97.11 timescale db instance")
            start_ins(instance_dict['tsdb'])
            send_mail("tsdb" + ' ' + "34.196.97.11 IOT instance has been started by" + ' ', user)
    elif sys.argv[2] == "iot_dep_server":
        if ins_status(instance_dict['iot_dep_server']) == "running" or ins_status(instance_dict['iot_dep_server']) == "pending":
            print("IOT deployment server is already in running state and please check mail about who has started")
        else:
            print ("starting 34.224.227.64 IOT Deployment server")
            start_ins(instance_dict['iot_dep_server'])
            send_mail("iot_dep_server" + ' ' + "34.224.227.64 IOT instance has been started by" + ' ', user )
    elif sys.argv[2] == "all":
        for k,v in instance_dict.items():
            if ins_status(v) == "running" or ins_status(v) == "pending":
                print ( k + ' ' + "instance is already in running state and please check mail about who has started")
            else:
                print (k + "IOT instance is being started")
                start_ins(v)
                send_mail(k + ' ' + "IOT instance has been started by" + ' ', user)
    else:
        print ("python3.4 ec2_start_stop.py start|stop {superset,tsdb,iot_dep_server,all")

elif sys.argv[1] == "stop":
    if sys.argv[2] == "superset":
        if ins_status(instance_dict['superset']) == "shutting-down" or ins_status(instance_dict['superset']) == "stopped" or ins_status(instance_dict['superset']) == "stopping":
            print ("superset instance is already in stopped state and please check mail about who has stopped")
        else:
            print ("stopping 34.231.254.23 superset instance")
            stop_ins(instance_dict['superset'])
            send_mail("superset" + ' ' + "34.231.254.23 IOT instance has been stopped by" + ' ', user)
    elif sys.argv[2] == "tsdb":
        if ins_status(instance_dict['tsdb']) == "shutting-down" or ins_status(instance_dict['tsdb']) == "stopped" or ins_status(instance_dict['tsdb']) == "stopping":
            print ("tsdb instance is already in stopped state and please check mail about who has stopped")
        else:
            print  ("stopping 34.196.97.11 tsdb instance")
            stop_ins(instance_dict['tsdb'])
            send_mail("tsdb" + ' ' + "34.196.97.11 IOT instance has been stopped by" + ' ', user)
    elif sys.argv[2] == "iot_dep_server":
        if ins_status(instance_dict['iot_dep_server']) == "shutting-down" or ins_status(instance_dict['iot_dep_server']) == "stopped" or ins_status(instance_dict['iot_dep_server']) == "stopping":
            print ("iot_dep_server instance is already in stopped state and please check mail about who has stopped")
        else:
            print ("stopping 34.224.227.64 IOT deployment server")
            stop_ins(instance_dict['iot_dep_server'])
            send_mail("iot_dep_server" +  ' ' + "34.224.227.64 IOT instance has been stopped by" + ' ', user)
    elif sys.argv[2] == "all":
        for k,v in instance_dict.items():
            if ins_status(v) == "shutting-down" or ins_status(v) == "stopped" or ins_status(v) == "stopping":
                #print (ins_status(v))
                print ( k + ' ' + "instance is already in stopped state and please check mail about who has started")
            else:
                print (k + ' ' + "IOT instance is being stopped")
                stop_ins(v)
                send_mail(k + ' ' + "IOT instance has been stopped by" + ' ', user)
    else:
        print ("python3.4 ec2_start_stop.py start|stop|status {superset,tsdb,iot_dep_server,all}")

elif sys.argv[1] == "status":
    if sys.argv[2] == "superset":
        if ins_status(instance_dict['superset']) == "running" or ins_status(instance_dict['superset']) == "pending":
            print ("superset 34.231.254.23 instance is running")
        elif ins_status(instance_dict['superset']) == "shutting-down" or ins_status(instance_dict['superset']) == "stopped" or ins_status(instance_dict['superset']) == "stopping":
            print ("Superset 34.231.254.23 instance has been stopped")
    elif sys.argv[2] == "tsdb":
        if ins_status(instance_dict['tsdb']) == "running" or ins_status(instance_dict['tsdb']) == "pending":
            print ("tsdb 34.196.97.11 instance is running")
        elif ins_status(instance_dict['tsdb']) == "shutting-down" or ins_status(instance_dict['tsdb']) == "stopped" or ins_status(instance_dict['tsdb']) == "stopping":
            print ("TSDB 34.196.97.11 instance has been stopped")
    elif sys.argv[2] == "iot_dep_server":
        if ins_status(instance_dict['iot_dep_server']) == "running" or ins_status(instance_dict['iot_dep_server']) == "pending":
            print ("iot_dep_server 34.224.227.64 instance is running")
        elif ins_status(instance_dict['iot_dep_server']) == "shutting-down" or ins_status(instance_dict['iot_dep_server']) == "stopped" or ins_status(instance_dict['iot_dep_server']) == "stopping":
            print ("iot_dep_server instance has been stopped")
    elif sys.argv[2] == "all":
        for k,v in instance_dict.items():
            if ins_status(v) == "running" or ins_status(v) == "pending":
                print ( k + ' ' + "instance is in running state")
            elif ins_status(v) == "shutting-down" or ins_status(v) == "stopped" or ins_status(v) == "stopping":
                print (k + ' ' + "instance is in stopped state")
    else:
        print ("python3.4 ec2_start_stop.py start|stop|status {superset,tsdb,iot_dep_server,all}")
else:
    print ("python3.4 ec2_start_stop.py start|stop|status {superset,tsdb,iot_dep_server,all}")
