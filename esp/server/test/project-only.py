#export SASHOME=/opt/sas/viya
#export PYTHONPATH="$SASHOME/home/SASEventStreamProcessingEngine/current/lib/:/app/python-esppy"

import os
import re
import sys
import time
import json
import errno
import socket
import signal
import logging
import argparse
import modelingApi
from subprocess import Popen
#from setproctitle import *
from multiprocessing import Process, Value, log_to_stderr
import csv
import esppy
from esppy.plotting import StreamingImages

def start_project():

    #astore path
    #astore_file='/shared/esp/DoD_warehouse/WAREHOUSE_Tiny-Yolov2.astore'
    astore_file=args.model
    #schema path
    #schema_file='/shared/esp/DoD_warehouse/WAREHOUSE_Tiny-Yolov2.astore.metadata'
    schema_file=args.schema

    def createYoloLabelString(file):
        astore_map = {}
        current_map='' #input_map: or output_map:
        with open(file, newline = '') as source:
            reader = csv.reader(source, delimiter='\t')
            for row in reader:
                if row[0] == 'input-map:':
                    astore_map[row[0]]=['id*:int64']
                    current_map=row[0]
                elif row[0] == 'output-map:':
                    astore_map[row[0]]=['id*:int64','_image_:blob']
                    #astore_map[row[0]].append('_image_:blob')
                    current_map=row[0]
                else:
                    #left,right = row[1].split(":")
                    left,right = re.split(': |\( |\)',row[1])
                    strip_txt=row[1].replace(" ", "")
                    astore_map[current_map].append(left+":"+right)
        return astore_map['output-map:']

    #host = os.environ['ESPHOST']
    #port = os.environ['ESPPORT']
    #host = 'espserver.esp19w25.local'
    #port = 30001

    # connect to the esp server
    try:
        esp = esppy.ESP('127.0.0.1', args.httpport)
    except Exception as e:
        print("Can't connect to ESP server: " + host)
        print(e)

    print(esp.server_info)

    #creating an empty project
    print("### Creating Project ###")
    detectionProject = esp.create_project('detectionProject')


    #adding source window
    src = esp.SourceWindow(schema=('id*:int64', 'image:blob'),
                              index_type='empty', insert_only=True)
    detectionProject.windows['w_data'] = src


    #adding resize window
    resize = esp.calculate.ImageProcessing(schema=('id*:int64', '_image_:blob'), function="resize", width=416, height=416)
    resize.set_inputs( imageInput='image:blob')
    resize.set_outputs( imageOutput='_image_:blob')
    detectionProject.windows['resized'] = resize


    #define a request window to inject the astore model to the reader window
    model_request = esp.SourceWindow(schema=('req_id*:int64', 'req_key:string', 'req_val:string'),
                                    index_type='empty', insert_only=True)
    detectionProject.windows['w_request'] = model_request


    #define a model reader window
    model_reader = esp.ModelReaderWindow()
    detectionProject.windows['w_reader'] = model_reader

    labelList = createYoloLabelString(schema_file)
    print(labelList)
    scorer = esp.ScoreWindow()
    scorer.schema = labelList
    scorer.add_offline_model(model_type='astore')
    detectionProject.windows['w_score'] = scorer

    #connecting the windows
    src.add_target( resize, role='data')
    resize.add_target( scorer, role='data')
    model_request.add_target( model_reader, role='request')
    model_reader.add_target( scorer, role='model')

    print("### Loading Project ###")
    #load the project
    esp.load_project(detectionProject)
    #print(detectionProject.to_xml(pretty=True))


    print("### Loading Model ###")
    #send the load model signal
    pub = model_request.create_publisher(blocksize=1, rate=0, pause=0,
                                   dateformat='%Y%m%dT%H:%M:%S.%f', opcode='insert', format='csv')
    pub.send('i,n,1,"action","load"\n')
    pub.send('i,n,2,"type","astore"\n')
    pub.send('i,n,3,"reference","' + astore_file + '"\n')
    pub.send('i,n,4,,\n')
    pub.close()

    print("### Project Started ###")


if __name__ == '__main__':
    # Read command line options
    argparser = argparse.ArgumentParser(description='Object Detection')
    argparser.add_argument('-m', dest='model', help='model (ASTORE) file', required=True)
    argparser.add_argument('-s', dest='schema', help='model schema file', required=True)
    argparser.add_argument('-p', dest='pubsub', help='ESP pubsub port number', type=int, required=True)
    argparser.add_argument('-a', dest='httpport', help='ESP http port number', type=int, required=False)
    argparser.add_argument('-d', dest='debug', help='enable debug', action="store_true")

    args = argparser.parse_args()

    # Enable debug
    logger = log_to_stderr()
    esp_log_level = 'fatal'
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger(modelingApi.getLoggingHandler()).setLevel(logging.DEBUG)
        esp_log_level = 'trace'
    else:
        logger.setLevel(logging.WARN)
        logging.getLogger(modelingApi.getLoggingHandler()).setLevel(logging.FATAL)

    start_project()
