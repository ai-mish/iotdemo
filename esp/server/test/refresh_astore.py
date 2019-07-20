#export SASHOME=/opt/sas/viya
#export PYTHONPATH="$SASHOME/home/SASEventStreamProcessingEngine/current/lib/:/app/python-esppy"

import os
import sys
import csv
import esppy

if __name__ == '__main__':

    astore_file='/app/iotdemo/astore/DoD_warehouse/yolov2.astore'
    for i in range(10):
        try:
            esp = esppy.ESP('127.0.0.1', 30001)
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
        print("Can't connect to ESP server: localhost")
        exit(1)

    projects = esp.get_projects()
    project = projects['detectionProject']
    src = project["contquery"]["w_request"]
    print("### Loading Model ###")
    #send the load model signal
    pub = src.create_publisher(blocksize=1, rate=0, pause=0,
                                   dateformat='%Y%m%dT%H:%M:%S.%f', opcode='insert', format='csv')
    pub.send('i,n,1,"action","load"\n')
    pub.send('i,n,2,"type","astore"\n')
    pub.send('i,n,3,"reference","' + astore_file + '"\n')
    pub.send('i,n,4,usegpuesp,1\n')
    pub.send('i,n,5,NDEVICES,1\n')
    pub.send('i,n,6,DEVICE0,0\n')
    pub.send('i,n,7,,\n')
    pub.close()
