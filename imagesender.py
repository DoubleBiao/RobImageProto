#! /usr/bin/python3
import pickle
import struct
import socket
import numpy as np

class RobProtoClient:
    """based on TCP(socket):
    (app)                 |(RobProtoClient)                                |(TCP)
                          |                                                |
       cmd,value,(image)<---- dict:{"cmd":cmd,"val":val}                   |
                          |         <---- pickle chunk + datalen(uint32)   |
                          |                  <----- chunck              <------- socket send
                          |                                                |
    
     ......

     (app)                |(RobProtoClient)                                |(TCP)
                          |                                                |
        ACK(string) ------------>    ACK(4 bytes)                 <------------  socket recv 
                          |                                                |
                          |                                                |
    """

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))
    #def send_data(self,data):   #send bytes stream
    #    assert type(data) == bytes,"data to be sent must be converted to bytes stream"
    #    self.socket.send(data)

    #    out = self.socket.recv(4).decode()
    #    print(out)
    #def send_image(self,im):
    #    self.send_data(im.tobytes())
    def get(self):
        lenchunk=b""
        while len(lenchunk) < 4:
            lenchunk += self.socket.recv(4)
        datalen = struct.unpack("I",lenchunk)[0]
        datachunk=b""
        while len(datachunk) < datalen:  #stop when receive the whole image
            data = self.socket.recv(8192)
            datachunk+=data

        datadict = pickle.loads(datachunk)
        return datadict["cmd"],datadict["val"]
    def ACK(self):
        self.socket.send("TEST".encode())

    def stop(self):
        self.socket.close()

    def __del__(self):
        self.socket.close()


if __name__ == "__main__":
    rawimg = np.ones((64,64,3),dtype=np.uint8)
    robot = RobProtoClient("127.0.0.1", 6666)
    
    for i in range(10):
        datadict,val = robot.get()
        ########### do something ################
        print(datadict)
        print(val)
        ##########################################
        robot.ACK()

    robot.stop()

