import websocket
import json
import cv2
#import cv2.cv2 as cv2
import numpy as np
import base64
from matplotlib import pyplot as plt
from random import randint
from threading import Thread

threads = []
#object_list = ['person','militaryvehicle','substation','staticvehicle']
object_list = ['all','militaryvehicle','staticvehicle','movingvehicle']
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter("output.avi",fourcc, 10.0, (1080,800))

#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

def on_message(ws, message):

    print("### Message received ###")

    data = json.loads(message)

    img = highlightImage(data)

    (h, w) = img.shape[:2]
    #console.log("h: %d w: %d" % (h,w))

    if img is not None:
        r = cv2.resize(img, (1080, 800))
        #r = cv2.resize(img, (800, 600))
        b,g,r = cv2.split(r)
        rgb = cv2.merge([r,g,b])
        out.write(rgb)
        cv2.imshow('YOLO 2', rgb)
        cv2.waitKey(1)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")
    out.release()
    cv2.destroyAllWindows()


def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(5)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


# utility functions
def highlightImage(data):

    row = data['events'][0]['event']
    numberOfObjects = data['events'][0]['event']['_nObjects_']
    print("Number of Objects: " + str(numberOfObjects))
    imageBufferBase64 = data['events'][0]['event']['_image_']['_image_']
    nparr = np.frombuffer(base64.b64decode(imageBufferBase64), dtype=np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image_h, image_w,_ = img_np.shape
    print(img_np.shape)
    for i in range(0, int(float(numberOfObjects))):

        obj = row['_Object' + str(i) + '_']
        prob = float(row['_P_Object' + str(i) + '_'])
        probability = "(" + str(round(prob * 100, 2)) + "%)"
        x = float(row['_Object' + str(i) + '_x'])
        y = float(row['_Object' + str(i) + '_y'])
        width = float(row['_Object' + str(i) + '_width'])
        height = float(row['_Object' + str(i) + '_height'])

        r = prob * 255
        b = randint(0, 255)
        g = randint(0, 255)

        x_min = int(image_w * (x - width / 2))
        y_min = int(image_h * (y - height/ 2))
        x_max = int(image_w * (x + width / 2))
        y_max = int(image_h * (y + height/ 2))
        #print("# of Object: " + str(numberOfObjects) + " name: " + str(obj.lower()) + " prob: " + str(prob))
        if 'all' in object_list:
                #print("X: " + str(x) + ", " + "Y: " + str(y) + ", " + "W: " + str(width) + ", " + "H: " + str(height))
                #if prob > 0.20:
                cv2.rectangle(img_np, (x_min, y_min), (x_max, y_max), (155, 255, 255), 1)
                cv2.putText(img_np, obj, (x_min, y_min), cv2.FONT_HERSHEY_SIMPLEX, 1e-3 * image_h, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(img_np, probability, (x_min, y_min + 20), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1e-3 * image_h, (255, 255, 255), 1,cv2.LINE_AA)
                print("# of Object: " + str(numberOfObjects) + " name: " + str(obj) + " prob: " + str(prob))
                print("x: " + str(x_min) + " y: " + str(y_min) + " width: " + str(x_max) + " height: " + str(y_max))
        else:
            if obj.lower() in object_list:
                #print("X: " + str(x) + ", " + "Y: " + str(y) + ", " + "W: " + str(width) + ", " + "H: " + str(height))
                #if prob > 0.20:
                cv2.rectangle(img_np, (x_min, y_min), (x_max, y_max), (155, 255, 255), 1)
                cv2.putText(img_np, obj, (x_min, y_min), cv2.FONT_HERSHEY_SIMPLEX, 1e-3 * image_h, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(img_np, probability, (x_min, y_min + 20), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1e-3 * image_h, (255, 255, 255), 1,cv2.LINE_AA)
                print("# of Object: " + str(numberOfObjects) + " name: " + str(obj) + " prob: " + str(prob))
                print("x: " + str(x_min) + " y: " + str(y_min) + " width: " + str(x_max) + " height: " + str(y_max))
            else:
                pass
    return img_np



if __name__ == "__main__":

    try:

        #websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://esp61.sasanzdemo.com:30001/SASESP/subscribers/detectionProject/contquery/w_score/?format=json&mode=streaming&pagesize=5&schema=true",
                                         on_message = on_message,
                                         on_error = on_error,
                                         on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()

    except KeyboardInterrupt:
        for thread in threads:
            thread.join()
