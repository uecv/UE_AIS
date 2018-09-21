#coding:utf-8
from socket import socket,AF_INET,SOCK_STREAM
from PIL import Image
import base64
from io import BytesIO
img = Image.open('/home/kenwood/Pictures/kenwood.jpg','r')
buffer = BytesIO()
img.save(buffer,format='JPEG')
raw_image = base64.b64encode(buffer.getvalue())

s= socket(AF_INET,SOCK_STREAM)
s.connect(('localhost',20000))
s.send(raw_image)
# print(s.recv(8192))