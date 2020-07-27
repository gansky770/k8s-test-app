#!/usr/bin/python3
import boto3
from pythonjsonlogger import jsonlogger
import logging
import datetime
import os


#define jsonlogger






class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log_record['timestamp'] = now
        if  not log_record.get('Running clusters'):
            log_record['Running clusters'] = 770
            #log_record['level'] = record.levelname

            

formatter = CustomJsonFormatter('(threadName)  (name) (timestamp) (Running clusters) (msecs) (message) (levelname) ',validate=False)
logHandler = logging.StreamHandler()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

    




#ec2 = boto3.resource('ec2')
## Boto3
## Use the filter() method of the instances collection to retrieve
## all running EC2 instances.
# instances = ec2.instances.filter(
#     Filters=[{'Name': 'tag:k8s.io/role/master', 'Values': ['1']},
#              {'Name': 'instance-state-code', 'Values': ['16']}])
# for instance in instances:
#     print(instance.id, instance.instance_type)



# {
#     "threadName": "MainThread",
#     "name": "K8S REPORTS",

#     "time": "04/08/2020",
#     "Running clusters": 3,
#     "CLUSTER 1 IP": 209.158.2.3,
#     "CLUSTER NAME": “K8S TESTING”,
#     "msecs": 506.24799728393555,
#     "message": "testing K8S REPORTING",
#     "levelname": "INFO",
# }
# ##default 
# {
#     "threadName": "MainThread",
#     "name": "root",
#     "thread": 140735202359648,
#     "created": 1336281068.506248,
#     "process": 41937,
#     "processName": "MainProcess",
#     "relativeCreated": 9.100914001464844,
#     "module": "tests",
#     "funcName": "testFormatKeys",
#     "levelno": 20,
#     "msecs": 506.24799728393555,
#     "pathname": "tests/tests.py",
#     "lineno": 60,
#     "asctime": ["12-05-05 22:11:08,506248"],
#     "message": "testing logging format",
#     "filename": "tests.py",
#     "levelname": "INFO",
#     "special": "value",
#     "run": 12
# }


logger.info('testing K8S REPORTING')
    