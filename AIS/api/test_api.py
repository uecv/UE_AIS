#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-8-21 下午3:45  
"""
import requests
from io import BytesIO
from PIL import Image
import os,base64
import cv2
import numpy as np
import io


detect_url = 'http://127.0.0.1:8888/face_detect'
add_url ='http://127.0.0.1:8888/add_face'
image_root='/home/kenwood/Pictures'
image_path ='test.jpeg'
img = Image.open(os.path.join(image_root,image_path), 'r')
buffered = BytesIO()
img.save(buffered, format="JPEG")
raw_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
print(raw_image)
#添加人脸
# data= {'face':raw_image,'name':'kevice','company':'yy','worker_id':'008'}
#验证人脸
data={'image':raw_image}
content = requests.post(detect_url,data=data)
# os.system("curl -X POST '127.0.0.1:8888/face_detect' -F 'image={}'".format(raw_image))
# frame = cv2.imdecode(np.frombuffer(base64.b64decode(raw_image), np.uint8), -1)
# faceDetect = MTCNNDetection(mtcnnDeteModel)
# locations, landmarks = faceDetect.detect(frame)
# print (locations)