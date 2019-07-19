# iotdemo


# push changes to master branch
```
git add .
git commit -m "comments"
git push -u origin master
```

# deploy code

```
sudo mkdir -p /app

cd /app
git clone https://github.com/sukmmi/iotdemo.git
cd iotdemo
git pull origin master
sudo chown -R ec2-user:ec2-user /app
```

# ESP server Install

```
source /opt/sas/os/anaconda3/bin/activate
conda init
sudo cp -p SASViyaV0300_09PCY1_Linux_x86-64.txt /opt/sas/viya/home/SASEventStreamProcessingEngine/6.1/etc/license/license.txt
sudo chown sas:sas /opt/sas/viya/home/SASEventStreamProcessingEngine/6.1/etc/license/license.txt
```

# ESP server start
```
export astore_dir=/app/iotdemo/astore/DoD_warehouse
bash /app/iotdemo/esp/server/objectdetection-server.sh -a 30001 -p 30003 -m $astore_dir/yolov2.astore -s $astore_dir/schema.txt

export astore_dir=/app/iotdemo/astore/DoD_DroneWebcam
python /app/iotdemo/esp/server/test/project-only.py -a 30001 -p 30003 -m $astore_dir/yolov2.astore -s $astore_dir/schema.txt
```
# ESP client installation

```
conda install -y pandas pillow ws4py requests graphviz plotly
git clone https://github.com/sassoftware/python-esppy.git
conda install websocket
conda install websocket-client
conda install -y --verbose -c conda-forge opencv==3.4.1
```

# stream.py

# display.py
