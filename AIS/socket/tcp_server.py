#coding:utf-8
from socketserver import BaseRequestHandler,TCPServer
import base64
import cv2
import numpy as np
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

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print("Got connection from",self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            frame = cv2.imdecode(np.frombuffer(base64.b64decode(msg.decode('utf-8')), np.uint8), -1)
            print('frame',frame)
            locations, landmarks = faceDetect.detect(frame)
            print(locations)

            if locations:
                # ** 人脸特征抽取
                # features_arr：人脸特征    positions：人脸姿态
                features_arr, positions = faceFeature.Extract(
                    frame, locations, landmarks)

                # ** 人脸识别/特征比对
                # Todo 改写查询数据库
                face_id = Recognition.Recognit(
                    known_face_dataset, features_arr, positions)
                print(face_id)
                self.request.send(face_id)

if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    serv.serve_forever()
# if __name__ == '__main__':
#     from threading import Thread
#     NWORKERS = 16
#     serv = TCPServer(('', 20000), EchoHandler)
#     for n in range(NWORKERS):
#         t = Thread(target=serv.serve_forever)
#         t.daemon = True
#         t.start()
#     serv.serve_forever()
