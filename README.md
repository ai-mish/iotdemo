# iotdemo

The aim of this project is to do real-time object detection using Yolov2 Model and take appropriate action.

## Python setup on ESP

```
source /opt/sas/os/anaconda3/bin/activate
conda init
```

## ESP license update
```
sudo cp -p SASViyaV0300_09PCY1_Linux_x86-64.txt /opt/sas/viya/home/SASEventStreamProcessingEngine/6.1/etc/license/license.txt
sudo chown sas:sas /opt/sas/viya/home/SASEventStreamProcessingEngine/6.1/etc/license/license.txt
```

## ESP server start
Check esp section

## ESP client installation

```
conda install -y pandas pillow ws4py requests graphviz plotly
git clone https://github.com/sassoftware/python-esppy.git
conda install websocket
conda install websocket-client
conda install -y --verbose -c conda-forge opencv==3.4.1
```

## GPU monitor

```
watch -n 1 nvidia-smi
```

## Deploy code

```
sudo mkdir -p /app
cd /app
git clone https://github.com/sukmmi/iotdemo.git
cd iotdemo
git pull origin master
sudo chown -R ec2-user:ec2-user /app


sudo chmod 0755 /app/iotdemo/esp/server/*.sh
```

# Push changes to master branch
```
git add .
git commit -m "comments"
git push -u origin master
```
