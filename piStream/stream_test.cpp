//Original by Chris Dahms
//Example from https://github.com/MicrocontrollersAndMore/OpenCV_3_Windows_10_Installation_Tutorial
//Modified by Brian Do
//https://github.com/bdelta
//https://thenextepoch.blogspot.com/


#include<opencv2/core/core.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>

#include<iostream>

///////////////////////////////////////////////////////////////////////////////////////////////////
int main() {
    std::cout << "Connecting to rpi camera\n";
    std::cout << "Please run stream command on rpi!\n";
    cv::VideoCapture cap("./fifo264");     

    if (cap.isOpened() == false) {                                // check if VideoCapture object was associated to webcam successfully
        std::cout << "error: stream not accessed successfully\n\n";      // if not, print error message to std out                                                        // may have to modify this line if not using Windows
        return(0);                                                          // and exit program
    }
    std::cout << "Connected!\n";

    cv::Mat imgOriginal;        // input image
    cv::Mat imgGrayscale;       // grayscale of input image
    cv::Mat imgBlurred;         // intermediate blured image
    cv::Mat imgCanny;           // Canny edge image

    char charCheckForEscKey = 0;

    while (charCheckForEscKey != 27 && cap.isOpened()) {            // until the Esc key is pressed or webcam connection is lost
        bool blnFrameReadSuccessfully = cap.read(imgOriginal);            // get next frame

        if (!blnFrameReadSuccessfully || imgOriginal.empty()) {                 // if frame not read successfully
            std::cout << "error: frame not read from stream\n";                 // print error message to std out
            break;                                                              // and jump out of while loop
        }

        cv::cvtColor(imgOriginal, imgGrayscale, CV_BGR2GRAY);                   // convert to grayscale

        cv::GaussianBlur(imgGrayscale,              // input image
                         imgBlurred,                // output image
                         cv::Size(5, 5),            // smoothing window width and height in pixels
                         1.8);                      // sigma value, determines how much the image will be blurred

        cv::Canny(imgBlurred,                       // input image
                  imgCanny,                         // output image
                  50,                               // low threshold
                  100);                             // high threshold

                                                    // declare windows
        cv::namedWindow("imgOriginal", CV_WINDOW_NORMAL);       // note: you can use CV_WINDOW_NORMAL which allows resizing the window
        cv::namedWindow("imgCanny", CV_WINDOW_NORMAL);          // or CV_WINDOW_AUTOSIZE for a fixed size window matching the resolution of the image
                                                                // CV_WINDOW_AUTOSIZE is the default
        cv::imshow("imgOriginal", imgOriginal);                 // show windows
        cv::imshow("imgCanny", imgCanny);                       //

        charCheckForEscKey = cv::waitKey(1);        // delay (in ms) and get key press, if any
	}   // end while

	return(0);
}
