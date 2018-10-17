import cv2
import sys


helpText = "'q' to Quit, 's' to start select bounding box then press enter when done"
help2 = "coordinate print on console"
font = cv2.FONT_HERSHEY_PLAIN

#cap = cv2.VideoCapture(0)
gst_str = ("v4l2src device=/dev/video{} ! "
               "video/x-raw, width=(int){}, height=(int){}, format=(string)RGB ! "
               "videoconvert ! appsink").format(1, 1280, 720)
cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    sys.exit("Failed to open camera!")


# initialize the bounding box coordinates of the object we are going to track
initBB = None

while True:
    ret, frame = cap.read()

    if frame is None:
        print("Can't find frame")
        break

    # get frame dimension
    (H, W) = frame.shape[:2]

    # display
    cv2.putText(frame, helpText, (11, 20), font, 1.0, (32, 32, 32), 4, cv2.LINE_AA)
    cv2.putText(frame, helpText, (10, 20), font, 1.0, (240, 240, 240), 1, cv2.LINE_AA)
    cv2.putText(frame, help2, (11, 450), font,1.0, (32, 32, 32), 4, cv2.LINE_AA)
    cv2.putText(frame, help2, (10, 450), font, 1.0, (240, 240, 240), 1, cv2.LINE_AA)
    cv2.imshow("Frame", frame)

    # wait for key to press
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                               showCrosshair=True)
        print("Bounding box\n")
        print("X Y Height Width " + str(initBB))
        print("Frame Dimension: Height " + str(H) + " Width " + str(W) + "\n")

        initBB = None

    if key == ord("q"):
        break;


