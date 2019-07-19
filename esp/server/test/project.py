#!/usr/bin/env python
# coding: utf-8

# In[114]:


#imports
#import cv2
#import cv2.cv2 as cv2
import sys
#import base64
#import matplotlib
#import matplotlib.pyplot as plt
#import numpy as np
import csv
#import pprint as pp;


# In[115]:


sys.path.append("/vagrant/esp_19w25/git/python-esppy")
import esppy
from esppy.plotting import StreamingImages
sys.path.append("/vagrant/esp_19w25/git/python-swat")

#astore path
astore_file='/shared/esp/DoD_warehouse/WAREHOUSE_Tiny-Yolov2.astore'
#schema path
schema_file='/vagrant/esp_19w25/git/esp/DoD_warehouse/WAREHOUSE_Tiny-Yolov2.astore.metadata'

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
                strip_txt=row[1].replace(" ", "")
                astore_map[current_map].append(strip_txt)
    return astore_map['output-map:']

#host = os.environ['ESPHOST']
#port = os.environ['ESPPORT']
host = 'espserver.esp19w25.local'
port = 30001

# connect to the esp server
try:
    esp = esppy.ESP(host, 30001)
except Exception as e:
    print("Can't connect to ESP server: " + host)
    print(e)


# In[103]:
print(esp.server_info)

#creating an empty project
print("### Creating Project ###")
detectionProject = esp.create_project('detectionProject')


# In[107]:
#adding source window
src = esp.SourceWindow(schema=('id*:int64', 'image:blob'),
                          index_type='empty', insert_only=True)
detectionProject.windows['w_data'] = src


# In[108]:
#adding resize window
resize = esp.calculate.ImageProcessing(schema=('id*:int64', '_image_:blob'), function="resize", width=416, height=416)
resize.set_inputs( imageInput='image:blob')
resize.set_outputs( imageOutput='_image_:blob')
detectionProject.windows['resized'] = resize


# In[109]:


#define a request window to inject the astore model to the reader window
model_request = esp.SourceWindow(schema=('req_id*:int64', 'req_key:string', 'req_val:string'),
                                index_type='empty', insert_only=True)
detectionProject.windows['w_request'] = model_request


# In[110]:


#define a model reader window
model_reader = esp.ModelReaderWindow()
detectionProject.windows['w_reader'] = model_reader


# In[111]:


#add a scoring window
#labelList = createYoloLabelString()
#server path
#astore_file='/shared/esp/DoD_warehouse/WAREHOUSE_Tiny-Yolov2.astore'
astore_file='/shared/esp/DoD_DroneSpotter/DroneSpotter_Tiny-Yolov2.astore'
#local path
#schema_file='/vagrant/esp_19w25/git/esp/DoD_warehouse/WAREHOUSE_Tiny-Yolov2.astore.metadata'
schema_file='/vagrant/esp_19w25/git/esp/DoD_DroneSpotter/schema.txt'

labelList = createYoloLabelString(schema_file)
scorer = esp.ScoreWindow()
scorer.schema = labelList
scorer.add_offline_model(model_type='astore')
detectionProject.windows['w_score'] = scorer

#add aggregate window
#agg = esp.AggregateWindow(schema=('id*:int64', 'cOut:double'),
#                          pubsub=True)
#agg.add_field_expressions('ESP_aAve(cOut)')
#detectionProject.windows['w_agg'] = agg

# In[112]:
#<window-transpose name="TransposeL" pubsub="true" mode="long" tag-name="TAG" tag-values="value,time" tags-included="pitch,roll,yaw,velocity">

#connecting the windows
src.add_target( resize, role='data')
resize.add_target( scorer, role='data')
model_request.add_target( model_reader, role='request')
model_reader.add_target( scorer, role='model')


# In[96]:

print("### Loading Project ###")
#load the project
esp.load_project(detectionProject)
#print(trades_project.to_xml(pretty=True))

# In[113]:

print("### Loading Model ###")
#send the load model signal
pub = model_request.create_publisher(blocksize=1, rate=0, pause=0,
                               dateformat='%Y%m%dT%H:%M:%S.%f', opcode='insert', format='csv')
pub.send('i,n,1,"action","load"\n')
pub.send('i,n,2,"type","astore"\n')
pub.send('i,n,3,"reference","' + astore_file + '"\n')
pub.send('i,n,4,,\n')
pub.close()

print("### Project Started - python stream.py ###")
