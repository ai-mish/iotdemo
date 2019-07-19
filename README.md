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
sudo chown ec2-user:ec2-user /app
cd /app
git clone https://github.com/sukmmi/iotdemo.git
cd iotdemo
git pull origin master
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
