#!/usr/bin/python3
import boto3
import random
from pythonjsonlogger import jsonlogger 
import logging
import datetime
import time
from decouple import config
#define runtime parametr from config (.ENV)
runtime = config('RUNTIME')
mockup = config('MOCKUP')
region = boto3.session.Session().region_name
while True:
    #formatter construct
    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def add_fields(self, log_record, record, message_dict):
            #super(CustomJsonFormatter, self).add_fields(log_record,record, message_dict )
            log_record['line'] = record.message
            log_record['loglevel'] = record.levelname
            if not log_record.get('timestamp'):
                now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                log_record['timestamp'] = now
            if  not log_record.get('Running instances'):
                if mockup=='TRUE': #if mockup ,random number of instances 0-50
                    log_record['Running instances'] = int(random.randrange(0,65,1))
                else: #real aws instances
                    log_record['Running instances'] = int(len(instances_info)/2)   
            if  not log_record.get('region'):
                log_record['region'] = region

    #extra dict-instances info acamulator   
    instances_info={}
    #test function for loogin info update
    def running_instances_mockup():
        i=0
        #imulate  instances dict
        running_instances={'aws-instance'+str(random.randrange(1, 100,1))+'':'192.168.254.'+str(random.randrange(1, 100,1))+'','aws-instances'+str(random.randrange(1, 100,1))+'':'192.168.111.'+str(random.randrange(1, 100,1))+'','aws-instances'+str(random.randrange(1, 100,1))+'':'192.168.116.'+str(random.randrange(1, 100,1))+''}
        for instance in running_instances:
            i+=1
            ip=running_instances[instance] #instance.private_ip_address
            name=instance #instace.state['Name']
            instances_info['instance_'+str(i)+'_IP']=ip
            instances_info['instance_'+str(i)+'_Name']=name   
    
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
            instances_info['instance'+str(i)+'_IP']=ip
            instances_info['instance'+str(i)+'_Name']=name                
#define formatter for the log messages (base on class CustomJsonFormatter )
    formatter =CustomJsonFormatter('%(region)s  - %(timestamp)s  -  %(line)s - %(loglevel)s -%(Running instances)s')
#formatter=pythonjsonlogger.jsonlogger.JsonFormatter(format_str)

#define jsonlogger
    
    logHandler = logging.StreamHandler()
    logHandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    if mockup=='TRUE':
        running_instances_mockup()
    else:
        running_instances_info()     
    logger.info('Running instances for region:'+region+'')
    
    
# define time to run
    time.sleep(int(runtime))
    #
     

    
     
    






    
