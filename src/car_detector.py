'''
This file drives the object tracker trained by the OpenCV library.
To do this, the .xml file returned by model training is used as a 
Cascade classifier and rectangular boxes are drawn around the predicted
region(s) of interest.

Created by Matthew Johnson 09/17/18 
'''
import numpy as np
import cv2

rc_car_cascade10 = cv2.CascadeClassifier('/home/nvidia/OpenCV/Collaborative-Sensing/model/cascade.xml')
#cap = cv2.VideoCapture(0)
gst_str = ("v4l2src device=/dev/video{} ! "
               "video/x-raw, width=(int){}, height=(int){}, format=(string)RGB ! "
               "videoconvert ! appsink").format(1, 1280, 720)
cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
i=0

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2



while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # add this
    # image, reject levels level weights.
    rc_cars = rc_car_cascade10.detectMultiScale(gray, scaleFactor=50, minNeighbors=50)
    
    # add this
    i=0

    for (x,y,w,h) in rc_cars:
	i+=1
        if(i>0 and i<17):
          cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)

          cv2.putText(img,str(i), 
            (x,y), 
            font, 
            fontScale,
            fontColor,
            lineType) 
          roi_gray = gray[y:y+h, x:x+w]
          roi_color = img[y:y+h, x:x+w]

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
