#!/usr/bin/python3
import sys
import boto3
from pythonjsonlogger import jsonlogger 
import logging
import datetime
import time
from decouple import config
#define runtime parametr from config (.ENV)
runtime = config('RUNTIME')

while True:
    #formatter constructor
    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def add_fields(self, log_record, record, message_dict):
            #super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
            if not log_record.get('timestamp'):
                now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                log_record['timestamp'] = now
                if  not log_record.get('Running clusters'):
                    log_record['Running clusters'] = int(len(cluster_info)/2)
                if log_record.get('name'):
                    log_record['name'] ='K8S REPORTS'   
    #extra dict-cluster info acamulator   
    cluster_info={}
    #test function for loogin info update
    def running_cluster_info_test():
        i=0
        running_instances={'aws-cluster':'192.168.254.16','aws-cluster770880990':'192.168.111.16','aws-cluster23232':'192.168.116.16'}
        for instance in running_instances:
            i+=1
            ip=running_instances[instance] #instance.private_ip_address
            name=instance #instace.state['Name']
            cluster_info['Cluster_'+str(i)+'_IP']=ip
            cluster_info['Cluster_'+str(i)+'_Name']=name   
    
#integrate boto3
# Use the filter() method of the instances collection to retrieve
# all running EC2 instances.
    def running_cluster_info():
        i=0 
        ec2 = boto3.resource('ec2')
        running_instances = ec2.instances.filter(
            Filters=[{'Name': 'tag:k8s.io/role/master', 'Values': ['1']},
                     {'Name': 'instance-state-code', 'Values': ['16']}])
        for instance in running_instances:
            i+=1
            ip=instance.private_ip_address
            name=instance.state['Name']
            cluster_info['Cluster'+str(i)+'_IP']=ip
            cluster_info['Cluster'+str(i)+'_Name']=name                
#define formatter for the log messages (base on class CustomJsonFormatter )
    formatter =CustomJsonFormatter('%(threadName)s  - %(name)s - %(timestamp)s  - %(msecs)s -  %(message)s - %(levelname)s -%(Running clusters)s')
#formatter=pythonjsonlogger.jsonlogger.JsonFormatter(format_str)

#define jsonlogger
    logHandler = logging.StreamHandler(sys.stdout)
    logHandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    running_cluster_info_test()
    #running_cluster_info() 
    logger.info('testing K8S REPORTING',extra=cluster_info)
# define time to run
    time.sleep(int(runtime))
     







    
