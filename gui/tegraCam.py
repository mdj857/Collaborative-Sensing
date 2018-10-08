#python3 tegra-cam.py --usb --vid 1 --width 1280 --height 720

# --------------------------------------------------------
# Camera sample code for Tegra X2/X1
#
# This program could capture and display video from
# IP CAM, USB webcam, or the Tegra onboard camera.
# Refer to the following blog post for how to set up
# and run the code:
#   https://jkjung-avt.github.io/tx2-camera-with-python/
#
# Written by JK Jung <jkjung13@gmail.com>
# --------------------------------------------------------

import numpy as np
import cv2


def open_cam_usb(dev, width, height):
    # We want to set width and height here, otherwise we could just do:
    #     return cv2.VideoCapture(dev)
    gst_str = ("v4l2src device=/dev/video{} ! "
               "video/x-raw, width=(int){}, height=(int){}, format=(string)RGB ! "
               "videoconvert ! appsink").format(dev, width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

def open_window(windowName, width, height):
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, width, height)
    cv2.moveWindow(windowName, 0, 0)
    cv2.setWindowTitle(windowName)

def read_cam(windowName, cap):
    showHelp = True
    showFullScreen = False
    helpText = "'Esc' to Quit, 'H' to Toggle Help, 'F' to Toggle Fullscreen"
    font = cv2.FONT_HERSHEY_PLAIN
    while True:
        if cv2.getWindowProperty(windowName, 0) < 0: # Check to see if the user closed the window
            # This will fail if the user closed the window; Nasties get printed to the console
            break;
        ret_val, displayBuf = cap.read();
        if showHelp == True:
            cv2.putText(displayBuf, helpText, (11,20), font, 1.0, (32,32,32), 4, cv2.LINE_AA)
            cv2.putText(displayBuf, helpText, (10,20), font, 1.0, (240,240,240), 1, cv2.LINE_AA)
        cv2.imshow(windowName, displayBuf)
        key = cv2.waitKey(10)
        if key == 27: # ESC key: quit program
            break
        elif key == ord('H') or key == ord('h'): # toggle help message
            showHelp = not showHelp
        elif key == ord('F') or key == ord('f'): # toggle fullscreen
            showFullScreen = not showFullScreen
            if showFullScreen == True:
                cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            else:
                cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)