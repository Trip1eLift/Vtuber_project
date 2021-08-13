import socket
import time
import json

HEADERSIZE = 10
HOST = "127.0.0.1"
PORT = 5002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
frame = 1

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    package = "Welcome to the server!"
    jpack = {'fps': 1, 'frame': frame, 'payload': package}
    msg = json.dumps(jpack)
    msg = f"{len(msg):<{HEADERSIZE}}"+msg

    clientsocket.send(bytes(msg,"utf-8"))
    frame = frame + 1

    while True:
        time.sleep(3)
        package = f"The time is {time.time()}"
        jpack = {'fps': 1, 'frame': frame, 'payload': package}
        msg = json.dumps(jpack)
        msg = f"{len(msg):<{HEADERSIZE}}"+msg

        print(msg)

        clientsocket.send(bytes(msg,"utf-8"))
        frame = frame + 1
        