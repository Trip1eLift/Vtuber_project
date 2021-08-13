#!/usr/bin/env python3

import socket
import json
import time

HEADERSIZE = 10
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5002        # The port used by the server

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((HOST, PORT))

while True:
    full_pack = ''
    new_pack = True
    while True:
        pack = soc.recv(10)
        if new_pack:
            print("new pack len:", pack[:HEADERSIZE])
            packlen_str = pack[:HEADERSIZE]
            packlen = int(pack[:HEADERSIZE])
            new_pack = False

        #print(f"full pack length: {packlen}")

        full_pack += pack.decode("utf-8")

        #print(len(full_pack))

        if len(full_pack) - HEADERSIZE == packlen:
            print("full package recvd")
            pack = full_pack[HEADERSIZE:]
            #print(pack)
            jpackage = json.loads(pack)
            out = "frame: " + str(jpackage['frame']) + ", fps: " + str(jpackage['fps'])
            print(out)
            new_pack = True
            full_pack = ""
        


