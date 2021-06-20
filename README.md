# Vtuber_project
Attempting to make my own Vtubing engine using mostly C++

It requires OpenCV4.5 to run. (Better to use 3.4.10 to match mediapipe since the begining...)
https://opencv.org/releases/

It also requires mediapipe.
https://google.github.io/mediapipe/getting_started/install.html#installing-on-windows
mediapipe hand example:

-1. Do installer install opencv3.4.10 on c: IMPORTANT
0. In mediapipe repo
1. bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 --action_env PYTHON_BIN_PATH="C://Users//User//AppData//Local//Programs//Python//Python37//python.exe" 
2. mediapipe/examples/desktop/hand_tracking:hand_tracking_cpu
GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/hand_tracking/hand_tracking_cpu \
  --calculator_graph_config_file=mediapipe/graphs/hand_tracking/hand_tracking_desktop_live.pbtxt
  
