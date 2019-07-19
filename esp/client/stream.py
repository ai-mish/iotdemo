import cv2
#import cv2.cv2 as cv2
import sys
import base64
import time
import uuid
import os

sys.path.append("/vagrant/esp_19w25/git/python-esppy")
import esppy
from esppy.plotting import StreamingImages
sys.path.append("/vagrant/esp_19w25/git/python-swat")
import swat

#cap = cv2.VideoCapture(0)



host = 'espserver.esp19w25.local'
port = 30001

esp = esppy.ESP(host, 30001)
print(esp.server_info)
projects = esp.get_projects()
project = projects['detectionProject']
src = project["contquery"]["w_data"]

pub = src.create_publisher(blocksize=1, rate=0, pause=0,
                           dateformat='%Y%m%dT%H:%M:%S.%f', opcode='insert',
                           format='csv')

def single_img(file):
    count = 100004
    image = cv2.imread(file)
    f2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    retval, buffer = cv2.imencode('.jpg', f2)
    encoded_string = base64.b64encode(buffer)
    strToSend = "i, n, " + str(count) + "," + encoded_string.decode() + "\n"
    pub.send(strToSend)
    #print(strToSend)
    #count+=1
    print("Sent frame #" + str(count))

def multiple_img(dir):
    count = 50000
    for filename in os.listdir(dir):
        if filename.endswith(".jpg"):
             # print(os.path.join(directory, filename))
             image = cv2.imread(os.path.join(dir, filename))
             f2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
             retval, buffer = cv2.imencode('.jpg', f2)
             encoded_string = base64.b64encode(buffer)
             strToSend = "i, n, " + str(count) + "," + encoded_string.decode() + "\n"
             pub.send(strToSend)
             #print(strToSend)
             count+=1
             print("Sent image #" + str(os.path.join(dir, filename)))
             time.sleep(10)
        else:
            continue

def video():
    #cap = cv2.VideoCapture('/vagrant/esp_19w25/git/data/PremiseMonitoringV2_30FPS.mp4')
    #cap = cv2.VideoCapture('/vagrant/esp_19w25/git/data/WarehouseSearch.mp4')
    cap = cv2.VideoCapture('/vagrant/esp_19w25/git/data/WIN_20190718_15_49_29_Pro.mp4')

    if (cap.isOpened()== False):
        print("Error opening video stream or file")
        return
    video_length = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
    print("Number of frames: %s" % str(video_length))
    # ESP count must start from 1
    #count = 1
    count = 20000
    #while True:
    while cap.isOpened():
            ret, image = cap.read()
            f2 = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            _, buffer = cv2.imencode('.jpg', f2)
            encoded_string = base64.b64encode(buffer)
            strToSend = "i, n, " + str(count) + "," + encoded_string.decode() + "\n"
            pub.send(strToSend)
            #print(strToSend)
            print("Sent frame #" + str(count))
            count+=1
            # 10 frames per seconds
            time.sleep(0.04)
    #cap.release()

video()
#single_img('/vagrant/esp_19w25/git/data/test/ObjectDeteection-PremiseMonitoring2.mp4#t=0.1.jpg')
#multiple_img('/vagrant/esp_19w25/git/data/test')
