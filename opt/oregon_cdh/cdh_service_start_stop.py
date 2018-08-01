#!/bin/python
import time
import sys
from cm_api.api_client import ApiResource
from cm_api.endpoints.cms import ClouderaManager
import argparse

cm_host = "10.0.73.249"
cm_port = 7180
cm_username = "admin"
cm_password = "admin"

services = ['hive', 'yarn', 'spark_on_yarn', 'hdfs', 'zookeeper', 'hbase', 'solr', 'ks_indexer', 'oozie', 'spark2_on_yarn', 'hue']
#api = ApiResource(cm_host, username="admin", password="admin")
api = ApiResource(cm_host, cm_port, cm_username, cm_password, version=14)
cluster_name = "CDH"
cluster = api.get_cluster(cluster_name)
print 'cluster...=',cluster

def check_arg(args=None):
    parser = argparse.ArgumentParser(description='args : start/stop')
    parser.add_argument('-o', '--op',
                        help='operation type',
                        required='True',
                        default='stop')

    results = parser.parse_args(args)
    return (results.op)

def cdh_services(op):
    for c in api.get_all_clusters():
        print 'c.name = ', c.name
        for s in api.get_cluster(c.name).get_all_services():
            #print 's.name =', s.name
            if s.name in services:
              print "Found " + s.name + " service"
            else:
              print 'No such service' , s.name

        #cluster = api.get_cluster(cluster_name)
        cluster = api.get_cluster(c.name)
        print 'cluster2 =',cluster
        if op == 'stop':
            print 'cdh service - stop'
            cluster.stop().wait()
        elif op == 'start':
            print 'cdh service - start'
            cluster.start().wait()

def cdh_manager(op):
    cm = ClouderaManager(api)
    cm_service = cm.get_service()
    print 'cm_service=',cm_service
    #restart the management service
    if op == 'stop':
        print 'cm service - stop'
        cm_service.stop().wait()
    elif op == 'start':
        print 'cm service - start'
        cm_service.restart().wait()

if __name__ == '__main__':
    op = check_arg(sys.argv[1:])
    if op == 'start':
        cdh_manager(op)
        cdh_services(op)
    elif op == 'stop':
        cdh_services(op)
        cdh_manager(op)
