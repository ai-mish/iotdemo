import cv2
#import cv2.cv2 as cv2
import sys
import base64
import time
import uuid
import os

sys.path.append("/vagrant/esp_19w25/git/python-esppy")
import esppy


#host = 'espserver.esp19w25.local'
#port = 30001
host='esp61.sasanzdemo.com'
port = 80


def getUniqueId():
    id=str(uuid.uuid1().int>>96).strip()
    return id

def webcam():
    cap = cv2.VideoCapture(0)

    if (cap.isOpened()== False):
        print("Error opening video stream or file")
        return
    video_length = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
    print("Number of frames: %s" % str(video_length))
    while cap.isOpened():
            ret, image = cap.read()
            f2 = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            _, buffer = cv2.imencode('.jpg', f2)
            encoded_string = base64.b64encode(buffer)
            #id=str(uuid.uuid4())
            id=getUniqueId()
            print(id)
            strToSend = "i, n," + id + "," + encoded_string.decode() + "\n"
            pub.send(strToSend)
            #print(strToSend)
            print("Sent frame #" + str(count))
            count+=1
            # 10 frames per seconds
            time.sleep(0.04)
    #cap.release()

if __name__ == '__main__':

    for i in range(10):
        try:
            esp = esppy.ESP(host, port)
            print(esp.server_info)
        except Exception as e:
            print("Can't connect to ESP server: " + host)
            print(e)
            time.sleep(5)
            continue
            #exit(1)
        else:
            break
    else:
        print("Can't connect to ESP server: " + host)
        exit(1)

    projects = esp.get_projects()
    project = projects['detectionProject']
    src = project["contquery"]["w_data"]

    pub = src.create_publisher(blocksize=1, rate=0, pause=0,
                               dateformat='%Y%m%dT%H:%M:%S.%f', opcode='insert',
                               format='csv')
    webcam()
