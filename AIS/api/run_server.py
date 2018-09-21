#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-8-21 下午2:27  
"""
import tornado.httpserver
import tornado.web
import tornado.ioloop


from AIS.api.handler.face_detect import facedecetehandler
from AIS.api.handler.add_face import addfacehandler


def make_app():
    return tornado.web.Application([
        (r"/face_detect", facedecetehandler),
        (r'/add_face', addfacehandler),
    ])

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8888, '0.0.0.0')
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()