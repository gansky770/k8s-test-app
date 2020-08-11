#!/usr/bin/python3
import boto3
from pythonjsonlogger import jsonlogger 
import logging
import datetime
import time
from decouple import config
import sys
from flask import Flask ,render_template,url_for,jsonify
import json
from json2html import *
from io import StringIO

app = Flask(__name__)
@app.route("/")
def main():
    with open('clusterinfo.json', 'r') as myfile:
        data=myfile.read()
     #parse to json   
        jsonobj=json.dumps(data)
     # convert to html   
        #htmljson = (json2html.convert(json=jsonobj))
        rsp = StringIO()
        rsp.write("""<!doctype html>
<html>
<head>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
 
<!-- Optional theme -->
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css">
 
</head><body>
<!-- Latest compiled and minified JavaScript -->
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
""")
        rsp.write(json2html.convert(json=jsonobj, table_attributes="class=\"table table-bordered table-hover\""))
        rsp.write('</body></html>')
    #return  render_template('main.html',output={rsp.getvalue()},)
    return  json2html.convert(json=jsonobj,table_attributes="class=\"table table-bordered table-hover\"")
   
if __name__ == "__main__":
    app.run(debug=True)
   
logHandler = logging.FileHandler('clusterInfo.json')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logHandler)
#formatter constructor
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log_record['timestamp'] = now
            if  not log_record.get('Running clusters'):
                log_record['Running clusters'] = int(len(cluster_info)/2)
            if log_record.get('name'):
                log_record['name'] ='K8S REPORTS' 
formatter =CustomJsonFormatter('%(threadName)s  - %(name)s - %(timestamp)s  - %(msecs)s -  %(message)s - %(levelname)s -%(Running clusters)s')
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)

#define runtime parametr from config (.ENV)
runtime = config('RUNTIME')

while True:   
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
    running_cluster_info_test()
    #running_cluster_info() 
    logger.info('Testing K8S REPORTING',extra=cluster_info)
    # read file
#     with open('clusterinfo.json', 'r') as myfile:
#         data=myfile.read()
#      #parse to json   
#         jsonobj=json.dumps(data)
#      # convert to html   
#         htmljson = (json2html.convert(json=jsonobj))
#         print(htmljson)
#         rsp = StringIO()
#         rsp.write("""<!doctype html>
# <html>
# <head>
# <!-- Latest compiled and minified CSS -->
# <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
 
# <!-- Optional theme -->
# <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css">
 
# </head><body>
# <!-- Latest compiled and minified JavaScript -->
# <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
# """)
#         rsp.write(json2html.convert(json=jsonobj, table_attributes="class=\"table table-bordered table-hover\""))
#         rsp.write('</body></html>')
#         return 'text/html',rsp.getvalue()

    # define time to run
    time.sleep(int(runtime))
     
  






    
