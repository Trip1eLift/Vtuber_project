import cv2

fps = 60

def haarcascades_detection():
    mask = cv2.imread('source_image/Gura_portrait.jpg', cv2.IMREAD_UNCHANGED)
    vid = cv2.VideoCapture(0)
    cascade_classifier = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    if not vid.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = vid.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # print(frame.shape)
        frame = frame[90:390, 170:470]
        frame = cv2.flip(frame, 1)

        # Haarcascades detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade_classifier.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        enlarge_factor = 2
        frame = cv2.resize(frame, (frame.shape[0] * enlarge_factor, frame.shape[1] * enlarge_factor))
        cv2.imshow('webcam', frame)
        global fps
        if cv2.waitKey(int(1000 / fps)) >= 0:
            break

def dnn_detection():
    vid = cv2.VideoCapture(0)
    network = cv2.dnn.readNetFromCaffe('dnn/deploy.prototxt', 'dnn/res10_300x300_ssd_iter_140000.caffemodel')

    if not vid.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = vid.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # print(frame.shape)
        frame = frame[90:390, 170:470]
        frame = cv2.flip(frame, 1)

        # DNN detection
        blob = cv2.dnn.blobFromImage(frame)
        network.setInput(blob)
        outs = network.forward()
        for i in range(0, outs.shape[2]):
            confidence = outs[0, 0, i, 2]
            if confidence > 0.5:
                width = 300
                height = 300
                draw_x_start = int(outs[0, 0, i, 3] * width)
                draw_y_start = int(outs[0, 0, i, 4] * height)
                draw_x_end = int(outs[0, 0, i, 5] * width)
                draw_y_end = int(outs[0, 0, i, 6] * height)
                frame = cv2.rectangle(frame, (draw_x_start, draw_y_start), (draw_x_end, draw_y_end), (255, 0, 0), 2)

        enlarge_factor = 2
        frame = cv2.resize(frame, (frame.shape[0] * enlarge_factor, frame.shape[1] * enlarge_factor))
        cv2.imshow('webcam', frame)
        global fps
        if cv2.waitKey(int(1000 / fps)) >= 0:
            break

def gura_draw_over():
    mask = cv2.imread('source_image/Gura_portrait.jpg', cv2.IMREAD_UNCHANGED)
    mask = mask[700:2500, 900:2500]

    draw_x_start = 0
    draw_y_start = 0
    draw_x_end = 0
    draw_y_end = 0

    vid = cv2.VideoCapture(0)
    network = cv2.dnn.readNetFromCaffe('dnn/deploy.prototxt', 'dnn/res10_300x300_ssd_iter_140000.caffemodel')

    if not vid.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = vid.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # print(frame.shape)
        frame = frame[90:390, 170:470]
        frame = cv2.flip(frame, 1)

        # DNN detection
        blob = cv2.dnn.blobFromImage(frame)
        network.setInput(blob)
        outs = network.forward()
        for i in range(0, outs.shape[2]):
            confidence = outs[0, 0, i, 2]
            if confidence > 0.5:
                width = 300
                height = 300
                draw_x_start = int(outs[0, 0, i, 3] * width)
                draw_y_start = int(outs[0, 0, i, 4] * height)
                draw_x_end = int(outs[0, 0, i, 5] * width)
                draw_y_end = int(outs[0, 0, i, 6] * height)
                frame = cv2.rectangle(frame, (draw_x_start, draw_y_start), (draw_x_end, draw_y_end), (255, 0, 0), 2)

        enlarge_factor = 2
        frame = cv2.resize(frame, (frame.shape[0] * enlarge_factor, frame.shape[1] * enlarge_factor))
        draw_x_start = draw_x_start * enlarge_factor
        draw_y_start = draw_y_start * enlarge_factor
        draw_x_end = draw_x_end * enlarge_factor
        draw_y_end = draw_y_end * enlarge_factor
        mask = cv2.resize(mask, (draw_x_end - draw_x_start, draw_y_end - draw_y_start))
        frame[draw_y_start:draw_y_start + mask.shape[0], draw_x_start:draw_x_start + mask.shape[1], :] = mask[:, :, :]
        cv2.imshow('webcam', frame)
        global fps
        if cv2.waitKey(int(1000 / fps)) >= 0:
            break