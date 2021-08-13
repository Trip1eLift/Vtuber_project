# Goal:
# 1. Webcam setup
# 2. Face detection
# 3. Face mesh/landmark tracking

import face_detection as fd
import face_landmarks as fl
from time import sleep
from flask import Flask, Response
import asyncio

app = Flask(__name__)
#https://flask.palletsprojects.com/en/2.0.x/patterns/streaming/
HEADERSIZE = 10


@app.route('/')
def test():
    return '<h1>Hello world!<h1><br>' \
           '<h5>landmarks data is under "/stream"<br>' \
           'There are 468 landmarks per face, mapping can be found at: <br>' \
           'https://github.com/Trip1eLift/Vtuber_project/blob/main/mesh_map.jpeg<br>' \
           'JSON structure:<br>' \
           '{"fps": 6.153898944073454e-10, "frame": 0, <br>' \
           ' "payload": <br>' \
           '[{"landmark": {"x": 0.15502098202705383, "y": 0.6447156071662903, "z": -0.03037448413670063}},<br>' \
           '{"landmark": {"x": 0.14120766520500183, "y": 0.5946487188339233, "z": -0.07731606066226959}},<br>' \
           '{"landmark": {"x": 0.15068772435188293, "y": 0.6073617339134216, "z": -0.03643127158284187}}]<br>' \
           '...}<h5>'


@app.route("/hello")
def hello():
    return 'HELLO WORLD!!!'


@app.route('/yield')
def stream_data():
    def generate():
        num = -1
        while (True):
            num = num + 1
            msg = '<h1>Hello world!' + str(num) + '<h1>'
            msg = f'{len(msg): <{HEADERSIZE}}' + msg
            yield msg
    return Response(generate(), mimetype='text/html')


@app.route('/stream')
def stream_face_landmarks():
    return Response(fl.face_mesh_trace_json(), mimetype='application/json')


if __name__ == '__main__':
    #app.run()
    #fd.haarcascades_detection()
    #fd.dnn_detection()
    #fd.gura_draw_over()
    #fl.face_mesh_trace()
    fl.Socket_Server_face_mesh_trace_json()

