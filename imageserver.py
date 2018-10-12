#!/usr/bin/env python

from _thread import *
import socket
import sys
import numpy as np
import struct
import pickle
import sys

class RobProtoServer:
    def __init__(self,host,port,tot_socket):
        """based on TCP(socket):
                      
         .......
         (app)                |(RobProtoClient)                                |(TCP)
                              |                                                |
           cmd,value,(image) ----> dict:{"cmd":cmd,"val":val}                  |
                              |         ----> pickle chunk + datalen(uint32)   |
                              |                  -----> chunck              -------> socket send
                              |                                                |
        
         ......

         (app)                |(RobProtoClient)                                |(TCP)
                              |                                                |
            ACK(string)<----------------    ACK(4 bytes)         <----------------   socket recv 
                              |                                                |
                              |                                                |
        """
        self.list_sock = []
        for i in range(tot_socket):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            s.bind((host, port+i))
            s.listen(10)
            self.list_sock.append(s)
            print("[*] server listening on %s %d" %(host, (port+i)))


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
        cmd = "start"
        val = [20,30]
        while True:
            datadict = {"cmd":cmd,"val":val}
            datachunk = pickle.dumps(datadict)
            datalen = len(datachunk)
            lenchunk = struct.pack("I",datalen)
            chunk = lenchunk+datachunk
            try:
                conn.send(chunk)
            except BrokenPipeError:
                print("clinet stop")
                break
            ##### do something  ############
            val[0] = val[0] + 1
            ############################
       
            ACK = conn.recv(4).decode

    def __del__(self):
        for s in self.list_sock:
            s.close()

if __name__ == "__main__":
    ipaddress = ""
    startport = int(sys.argv[1])
    portnum = int(sys.argv[2])
    print("set up",portnum,"ports, start from:",startport)
    server = RobProtoServer(ipaddress,startport,portnum)
    server.setup()
