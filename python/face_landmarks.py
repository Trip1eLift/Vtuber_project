import cv2
import mediapipe as mp
import time


fps = 60

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

        enlarge_factor = 2
        frame = cv2.resize(frame, (frame.shape[1] * enlarge_factor, frame.shape[0] * enlarge_factor))

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) >= 0:
            break