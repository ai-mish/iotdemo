# iotdemo

The aim of this project is to deploy Yolov2 Model and provide API interface to interact.

#Setup Environment
```
sudo bash install.sh
```

#Start ESP
```
conda activate iotdemo
bash iotdemo/esp/server/objectdetection-server.sh -a 30003 -p 30004 -m iotdemo/astore/Yolov2_OutOfBox/Tiny-Yolov2.astore -s /iotdemo/astore/Yolov2_OutOfBox/schema.txt -d
```
