#! /usr/bin/python3

import socket
import numpy as np

class ImageSender:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))
    def send_data(self,data):   #send bytes stream
        assert type(data) == bytes,"data to be sent must be converted to bytes stream"
        self.socket.send(data)
    def send_image(self,im):
        self.send_data(im.tobytes())


    def __del__(self):
        self.socket.close()


if __name__ == "__main__":
    rawimg = np.ones((64,64,3),dtype=np.uint8)
    image_sender = ImageSender("127.0.0.1", 6666)
    image_sender.send_image(rawimg)

