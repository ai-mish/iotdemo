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
import csv
import esppy
from esppy.plotting import StreamingImages

def score():

    imgpath=args.imgpath

    # connect to the esp server
    try:
        esp = esppy.ESP('127.0.0.1', args.httpport)
    except Exception as e:
        print("Can't connect to ESP server: ")
        print(e)

    logger.info(esp.server_info)

    #creating an empty project
    logger.info("### Send Image ###")
    detectionProject = esp.create_project('detectionProject')

    #adding source window
    src = esp.SourceWindow(schema=('id*:int64', 'image:blob'),
                              index_type='empty', insert_only=True)
    detectionProject.windows['w_data'] = src


    #logger.info(labelList)
    scorer = esp.ScoreWindow()
    scorer.schema = labelList
    scorer.add_offline_model(model_type='astore')
    detectionProject.windows['w_score'] = scorer


    logger.info("### Project Started ###")


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Object Detection')
    argparser.add_argument('-i', dest='imgpath', help='Input Image full path', required=True)
    argparser.add_argument('-d', dest='debug', help='enable debug', action="store_true")

    args = argparser.parse_args()
    try:
        score(args.imgpath)
    # Clean up any child processes before exit
    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit:
        raise
