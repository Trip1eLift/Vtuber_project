#include "opencv2/opencv.hpp"
#include <vector>

const int fps = 60;

/*
Goal:
1. Webcam setup
2. Face detection
3. Face mesh/landmark tracking 
*/

int main(int argv, char **argc) 
{

	cv::Mat mask = cv::imread("source_image/Gura_portrait.jpg", cv::IMREAD_UNCHANGED);
	cv::Mat mask_temp;
	//cv::resize(mask, mask_temp, cv::Size((int)(mask.rows / 10), (int)(mask.cols / 10))); // 350x350
	//std::cout << mask_temp.rows << " " << mask_temp.cols << std::endl;
	cv::Rect mask_ROI(900, 700, 1600, 1800);
	mask = mask(mask_ROI);
	float draw_x_start, draw_y_start, draw_x_end, draw_y_end;

	cv::Mat frame;
	cv::VideoCapture vid(0);
	cv::CascadeClassifier cascade_classifier("haarcascades/haarcascade_frontalface_default.xml");
	cv::dnn::Net network = cv::dnn::readNetFromCaffe("dnn/deploy.prototxt", "dnn/res10_300x300_ssd_iter_140000.caffemodel");

	if (!vid.isOpened())
	{
		return -1;
	}

	while (vid.read(frame))
	{
		//std::cout << frame.rows << " " << frame.cols << std::endl; // 640x480
		// Region of Interest
		cv::Rect ROI(170, 90, 300, 300); 
		frame = frame(ROI);
		cv::flip(frame, frame, 1);
		
		// Haarcascades detection
		/*cv::Mat gray;
		cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
		std::vector<cv::Rect> faces;
		cascade_classifier.detectMultiScale(gray, faces, 1.1, 3, 0, cv::Size(30, 30), cv::Size(200, 200));
		if (faces.size() > 0) {
			cv::Point tl = faces[0].tl();
			cv::Point br = faces[0].br();
			cv::Scalar color(255, 0, 0);
			int thickness = 2;
			cv::rectangle(frame, tl, br, color, thickness);
		}*/

		// DNN detection
		cv::Mat blob = cv::dnn::blobFromImage(frame);
		network.setInput(blob);
		std::vector<cv::Mat> outs;
		network.forward(outs, "detection_out");
		CV_Assert(outs.size() > 0);
		for (size_t k = 0; k < outs.size(); k++)
		{
			float* data = (float*)outs[k].data;
			for (size_t i = 0; i < outs[k].total(); i += 7)
			{
				float confidence = data[i + 2];
				if (confidence > 0.5)
				{
					//Do something
					int width = 300, height = 300;
					float x_start = (int)(data[i + 3] * width);
					float y_start = (int)(data[i + 4] * height);
					float x_end = (int)(data[i + 5] * width);
					float y_end = (int)(data[i + 6] * height);
					cv::Scalar color(255, 0, 0);
					int thickness = 2;
					cv::rectangle(frame, cv::Point(x_start, y_start), cv::Point(x_end, y_end), color, thickness);
					
					// delay this
					draw_x_start = x_start;
					draw_y_start = y_start;
					draw_x_end = x_end;
					draw_y_end = y_end;
					//Draw over
					//cv::resize(mask, mask, cv::Size((int)(x_end - x_start), (int)(y_end - y_start)));
					//mask.copyTo(frame.rowRange(y_start, y_start + mask.rows).colRange(x_start, x_start + mask.cols)); // mask has to be jpg file
				}
			}
		}
		
		// Display
		float enlarge_factor = 2;
		cv::resize(frame, frame, cv::Size(frame.cols * enlarge_factor, frame.rows * enlarge_factor));
		// Delay drawing to avoid aliasing
		draw_x_start *= enlarge_factor;
		draw_y_start *= enlarge_factor;
		draw_x_end *= enlarge_factor;
		draw_y_end *= enlarge_factor;
		cv::resize(mask, mask, cv::Size((int)(draw_x_end - draw_x_start), (int)(draw_y_end - draw_y_start)));
		mask.copyTo(frame.rowRange(draw_y_start, draw_y_start + mask.rows).colRange(draw_x_start, draw_x_start + mask.cols));
		
		cv::imshow("webcam", frame);
		if (cv::waitKey(1000 / fps) >= 0)
			break;
	}

	return 1;
}

