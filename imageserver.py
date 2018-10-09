#!/usr/bin/env python

from _thread import *
import socket
import sys
import numpy as np


class ImageServer:
    def __init__(self,host,port,tot_socket,imagesize):
        self.list_sock = []
        for i in range(tot_socket):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            s.bind((host, port+i))
            s.listen(10)
            self.list_sock.append(s)
            print("[*] server listening on %s %d" %(host, (port+i)))
        self.imagesize = imagesize


    def setup(self):
        try:
            while 1:
                for s in self.list_sock:
                    conn, addr = s.accept()
                    print('[*] Connected with ' + addr[0] + ':' + str(addr[1]))
                    start_new_thread(self.clientthread ,(conn,))
        except KeyboardInterrupt as msg:
            pass


    def clientthread(self, conn):
        sbuffer=b""
        while len(sbuffer) < np.prod(self.imagesize):  #stop when receive the whole image
            data = conn.recv(8192)
            sbuffer+=data
        conn.close()
        recivedim = np.frombuffer(sbuffer,dtype=np.uint8).reshape(self.imagesize)
        print(recivedim.shape)

    def __del__(self):
        for s in self.list_sock:
            s.close()

if __name__ == "__main__":
    server = ImageServer('127.0.0.1',6666,2,(64,64,3))
    server.setup()
