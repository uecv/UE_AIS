#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-8-21 下午1:59  
"""
import tornado.httpserver
import tornado.web
import tornado.ioloop
import numpy as np
import cv2
import base64
from AIS.core.library.faceNetLib.faceNetFeatureLib import faceNetLib
from AIS.core.FaceDetection.MTCNNDetection import MTCNNDetection
from AIS.core.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from AIS.core.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
from AIS.settings import *

facelib = faceNetLib()
# 人脸特征库
known_face_dataset = facelib.getlib()

# 人脸识别接口
Recognition = faceNetRecognition()
# 人脸 检测接口
faceDetect = MTCNNDetection(mtcnnDeteModel)
# 人脸特征抽取接口
faceFeature = FaceNetExtract(faceNetModel)

class facedecetehandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        #x-www-form-urlencoded
        image = self.get_argument('image')
        print('image',image)
        company_id = self.get_argument('company_id')
        print ('company_id',company_id)
        frame = cv2.imdecode(np.frombuffer(base64.b64decode(image), np.uint8), -1)
        print ('frame',frame)
        locations, landmarks = faceDetect.detect(frame)
        print (locations)

        if locations:
            # ** 人脸特征抽取
            # features_arr：人脸特征    positions：人脸姿态
            features_arr, positions = faceFeature.Extract(
                frame, locations, landmarks)

            # ** 人脸识别/特征比对
            #Todo 改写查询数据库
            face_id = Recognition.Recognit(
                known_face_dataset, features_arr, positions)
            print (face_id)


