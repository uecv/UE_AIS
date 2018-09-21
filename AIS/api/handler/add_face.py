#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-8-21 下午2:34  
"""
import tornado.web
import base64
import cv2
import numpy as np
import io
from AIS.core.FaceDetection.MTCNNDetection import MTCNNDetection
from AIS.core.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from AIS.core.service import people as perpleDB
from AIS.core.service import features as featureDB
from AIS.settings import *
from PIL import Image



# 人脸 检测接口
faceDetect = MTCNNDetection(mtcnnDeteModel)
# 人脸特征抽取接口
faceFeature = FaceNetExtract(faceNetModel)


class addfacehandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        face = self.get_argument('face')
        name = self.get_argument('name')
        company = self.get_argument('company')
        worker_id = self.get_argument('worker_id')
        # base64 to np array
        print('message',face,name,company,worker_id)
        im = cv2.imdecode(np.frombuffer(base64.b64decode(face), np.uint8), -1)
        imgdata = base64.b64decode(str(face))
        image = Image.open(io.BytesIO(imgdata))
        image.save('/home/kenwood/图片/{}.jpg'.format(name))
        name_id ='/home/kenwood/图片/{}.jpg'.format(name)
        #信息入库
        people = perpleDB.People(name=name, image_path=name_id, company_id=company, worker_id=worker_id)
        perpleDB.insert_people(people)
        #抽特征入库
        locations, landmarks = faceDetect.detect(im)
        features_arr, positions = faceFeature.Extract(im, locations, landmarks)
        feature_str = base64.b64encode(features_arr.tostring()).decode("utf-8")
        featurebean = featureDB.Feature(people_id=people.id, feature=feature_str)
        featureDB.insert_feature(featurebean)



