#!/usr/bin/python3
import boto3
from botocore.config import Config
from pythonjsonlogger import jsonlogger 
import logging
import datetime
import time
from decouple import config
#define runtime parametr from config (.ENV)
runtime = config('RUNTIME')
moookup = config('MOOKUP')

while True:
    #formatter constructor
    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def add_fields(self, log_record, record, message_dict):
            super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
            if not log_record.get('timestamp'):
                now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                log_record['timestamp'] = now
                if  not log_record.get('Running instances'):
                    log_record['Running instances'] = int(len(instances_info)/2)
                if  not log_record.get('region'):
                    log_record['region'] = ""
    #extra dict-instances info acamulator   
    instances_info={}
    #test function for loogin info update
    def running_instances_mookup():
        
        i=0
        running_instances={'aws-instances':'192.168.254.16','aws-instances770880990':'192.168.111.16','aws-instances23232':'192.168.116.16'}
        for instance in running_instances:
            i+=1
            ip=running_instances[instance] #instance.private_ip_address
            name=instance #instace.state['Name']
            instances_info['instances_'+str(i)+'_IP']=ip
            instances_info['instances_'+str(i)+'_Name']=name   
    
#integrate boto3
# Use the filter() method of the instances collection to retrieve
# all running EC2 instances.
    def running_instances_info():
        i=0 
        ec2 = boto3.resource('ec2')
        running_instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-code', 'Values': ['16']}])
        for instance in running_instances:
            i+=1
            ip=instance.private_ip_address
            name=instance.state['Name']
            instances_info['instances'+str(i)+'_IP']=ip
            instances_info['instances'+str(i)+'_Name']=name                
#define formatter for the log messages (base on class CustomJsonFormatter )
    formatter =CustomJsonFormatter('%(region)s  - %(timestamp)s  -  %(message)s - %(levelname)s -%(Running instances)s')
#formatter=pythonjsonlogger.jsonlogger.JsonFormatter(format_str)

#define jsonlogger
    logHandler = logging.StreamHandler()
    logHandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    if moookup=='TRUE':
        running_instances_mookup()
    else:
        running_instances_info() 
    logger.info(0,extra=instances_info)
# define time to run
    time.sleep(int(runtime))
     

    
     
    # {"region": “eu-west-1”, "Running Instances": 5, "timestamp": "2016-08-08T16:21:43.177811", "loglevel": "info", "line": "Running instances for region: $REGION"}








    
