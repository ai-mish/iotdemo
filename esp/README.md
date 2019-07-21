# Start ESP server

## Premise
```
export astore_dir=/app/iotdemo/astore/DoD_Premise
bash /app/iotdemo/esp/server/objectdetection-server.sh -a 30001 -p 30002 -m $astore_dir/yolov2.astore -s $astore_dir/schema.txt
```

## Warehouse
```
export astore_dir=/app/iotdemo/astore/DoD_warehouse
bash /app/iotdemo/esp/server/objectdetection-server.sh -a 30003 -p 30004 -m $astore_dir/yolov2.astore -s $astore_dir/schema.txt
```

## Drone WebCam
```
export astore_dir=/app/iotdemo/astore/DoD_DroneWebcam
python /app/iotdemo/esp/server/test/project-only.py -a 30005 -p 30006 -m $astore_dir/yolov2.astore -s $astore_dir/schema.txt
```
##
```
sudo cp myservice.service /etc/systemd/system/myservice.service
sudo chmod 644 /etc/systemd/system/myservice.service
```
# Start client

## Stream

### Premise
```
python client/stream/premise.py
```

### Warehouse
```
python client/stream/warehouse.py
```

### Drone WebCam
```
python client/stream/dronwebcam.py
```
