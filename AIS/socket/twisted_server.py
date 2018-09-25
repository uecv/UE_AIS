#coding:utf-8
import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import  Protocol,ServerFactory,ClientFactory
import base64
import cv2
import numpy as np
from AIS.core.library.faceNetLib.faceNetFeatureLib import faceNetLib
from AIS.core.FaceDetection.MTCNNDetection import MTCNNDetection
from AIS.core.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from AIS.core.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
from AIS.settings import *
from PIL import Image
from io import BytesIO

facelib = faceNetLib()
# 人脸特征库
known_face_dataset = facelib.getlib()

# 人脸识别接口
Recognition = faceNetRecognition()
# 人脸 检测接口
faceDetect = MTCNNDetection(mtcnnDeteModel)
# 人脸特征抽取接口
faceFeature = FaceNetExtract(faceNetModel)

class EchoServerFactory(ServerFactory):
    """
    服务端工厂类
    """
    def buildProtocol(self, addr):
        return EchoServerProtocol()

class EchoClientFactory(ClientFactory):
    """
    客户端工厂类
    """
    def startedConnecting(self, connector):
        log.msg('Start the connect')

    def buildProtocol(self, addr):
        log.msg('Connected')
        return EchoClientProtocol()

    def clientConnectionLost(self, connector, reason):
        log.msg('Lost connection.Reason:{}'.format(reason))

    def clientConnectionFailed(self, connector, reason):
        log.msg('Lost failed.Reason:{}'.format(reason))

#添加协议
class EchoServerProtocol(Protocol):
    """
    服务端代码
    """
    def __init__(self):
        #规定数据大小
        self.__buffer = ""
        self.frame_size =91260
    def dataReceived(self, data):
        log.msg('Data received {}'.format(data))
        self.__buffer = self.__buffer + data.decode('utf-8')
        frame_size = self.frame_size
        print ('length',len(self.__buffer))
        while len(self.__buffer) >= frame_size:
            self.frame_received(self.__buffer[0:frame_size])
            self.__buffer = self.__buffer[frame_size:]

    def frame_received(self, data):
        """
        处理接受数据
        :param data: bytes
        :return:
        """
        #bytes to base64 to numpy array
        frame = cv2.imdecode(np.frombuffer(base64.b64decode(data), np.uint8), -1)
        print('frame', frame)
        #人脸检测，返回人脸位置
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
            print('face_id',face_id)
            # transport write must be bytes
            self.transport.write(bytes(face_id[0][0].encode('utf-8')))

    def connectionMade(self):
        log.msg('Client connection from {}'.format(self.transport.getPeer()))

    def connectionLost(self, reason):
        log.msg("Lost connection beacuse {}".format(reason))


class EchoClientProtocol(Protocol):
    """
    客户端代码
    """
    def connectionMade(self):
        img = Image.open('/home/kenwood/Pictures/kenwood.jpg', 'r')
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        raw_image = base64.b64encode(buffer.getvalue())
        # data = 'Hello Server!'
        self.transport.write(raw_image)
        log.msg('Data sent{}'.format(raw_image))
    def dataReceived(self, data):
        log.msg('Data received{}'.format(data))
        self.transport.loseConnection()

    def connectionLost(self, reason):
        log.msg('Lost connection because {}'.format(reason))

def main():
    log.startLogging(sys.stdout)
    log.msg('Start you engines')
    reactor.listenTCP(16000,EchoServerFactory())
    reactor.connectTCP('127.0.0.1',16000,EchoClientFactory())
    reactor.run()

if __name__ == '__main__':
    main()