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


app = Flask(__name__)
@app.route("/")
def main():
    with open('clusterinfo.json', 'r') as myfile:
        data=myfile.read()
    #parse to json   
        jsonobj=json.dumps(data)
#      # convert to html   
    return  json2html.convert(json=jsonobj,table_attributes="class=\"table table-bordered table-hover\"")
 #if __name__ == "__main__":
app.run('localhost',port=8000,debug=True)