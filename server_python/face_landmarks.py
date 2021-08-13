import cv2
import mediapipe as mp
import time
import json
import numpy
import socket
import asyncio

fps = 60
HEADERSIZE = 10

def face_mesh_trace():
    vid = cv2.VideoCapture(0)
    if not vid.isOpened():
        print("Cannot open camera")
        exit()

    mpDraw = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
    drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

    pTime = 0
    first_time = True
    while True:
        success, frame = vid.read()
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = frame[90:390, 170:470]
        frame = cv2.flip(frame, 1)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceMesh.process(frameRGB)
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                mpDraw.draw_landmarks(frame, faceLms, mpFaceMesh.FACE_CONNECTIONS,
                                      drawSpec, drawSpec)
            #if first_time:
            #    print(results.multi_face_landmarks[0].landmark[0])
            #    print(results.multi_face_landmarks)

        enlarge_factor = 2
        frame = cv2.resize(frame, (frame.shape[1] * enlarge_factor, frame.shape[0] * enlarge_factor))

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) >= 0:
            break


def face_mesh_trace_json():
    vid = cv2.VideoCapture(0)
    if not vid.isOpened():
        print("Cannot open camera")
        exit()

    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)

    frame_count = 0
    pTime = 0
    while True:
        success, frame = vid.read()
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = frame[90:390, 170:470]
        frame = cv2.flip(frame, 1)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceMesh.process(frameRGB)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        if results.multi_face_landmarks:
            package = []
            for index, mark in enumerate(results.multi_face_landmarks[0].landmark):
                landmark = {'x': mark.x, 'y': mark.y, 'z': mark.z}
                package.append({"landmark": landmark})
            frame_pack = {'fps': fps, 'frame': frame_count, 'payload': package}
            #jsonPack = json.dumps(package)
            jsonPack = json.dumps(frame_pack)

            jsonPack = f'{len(jsonPack): <{HEADERSIZE}}' + jsonPack
            yield jsonPack
        frame_count = frame_count + 1

    return 'TERMINATE'


def Socket_Server_face_mesh_trace_json():
    HOST = "127.0.0.1"
    PORT = 5001
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((HOST, PORT))
    soc.listen()

    vid = cv2.VideoCapture(0)
    if not vid.isOpened():
        print("Cannot open camera")
        exit()

    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)

    frame_count = 0
    pTime = 0

    clientsocket, address = soc.accept()
    print(f"Connection from {address} has been established.")

    while True:
        success, frame = vid.read()
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = frame[90:390, 170:470]
        frame = cv2.flip(frame, 1)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceMesh.process(frameRGB)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        if results.multi_face_landmarks:
            package = []
            for index, mark in enumerate(results.multi_face_landmarks[0].landmark):
                landmark = {'x': mark.x, 'y': mark.y, 'z': mark.z}
                package.append({"landmark": landmark})
            frame_pack = {'fps': fps, 'frame': frame_count, 'payload': package}
            jsonPack = json.dumps(frame_pack)
            pack_len = len(jsonPack)
            if pack_len == 0:
                continue
            jsonPack = f'{len(jsonPack): <{HEADERSIZE}}' + jsonPack
            print(jsonPack[:HEADERSIZE])
            print("frame:", frame_pack['frame'], "fps:", frame_pack['fps'])
            Send_package(clientsocket, jsonPack)
            #time.sleep(1)

        frame_count = frame_count + 1
        #print(frame_count)

    return 'TERMINATE'


def Send_package(clientsocket, package):
    # Socket connection
    clientsocket.send(bytes(package, "utf-8"))

