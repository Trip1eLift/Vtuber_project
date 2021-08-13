# Vtuber_project

## C++ (JUST IGNORE C++)
Attempting to make my own Vtubing engine using mostly C++
Attempt failed, no one use C++ for mediapipe

It requires OpenCV4.5 to run. (Better to use 3.4.10 to match mediapipe since the begining...)
https://opencv.org/releases/

It also requires mediapipe.
https://google.github.io/mediapipe/getting_started/install.html#installing-on-windows
mediapipe hand example:

-1. Do installer install opencv3.4.10 on c: IMPORTANT\
0. In mediapipe repo
1. bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 --action_env PYTHON_BIN_PATH="C://Users//User//AppData//Local//Programs//Python//Python37//python.exe" 
2. set GLOG_logtostderr=1
3. bazel-bin/mediapipe/examples/desktop/hand_tracking/hand_tracking_cpu "--calculator_graph_config_file=mediapipe/graphs/hand_tracking/hand_tracking_desktop_live.pbtxt"

## Python
uses PyCharm to import opencv-python, mediapipe, and flask. (Easy Peasy)

current version:

opencv-python 4.5.2.54
opencv-contrib-python 4.5.2.54
mediapipe 0.8.5

## Blender
use Blender 2.93
set port to 5002 for client_blender_python/socket_testing/socket_client.
set port to 5001 for server_python/main.py with face_landmarks.py library.

## Testing
client_blender_python/socket_testing/socket_server can tests client_blender_python/socket_testing/socket_client
client_blender_python/socket_testing/socket_client set to port 5001 can test server_python/main.py with face_landmarks.py library
