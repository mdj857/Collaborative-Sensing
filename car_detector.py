'''
This file drives the object tracker trained by the OpenCV library.
To do this, the .xml file returned by model training is used as a 
Cascade classifier and rectangular boxes are drawn around the predicted
region(s) of interest.

Created by Matthew Johnson 09/17/18 
'''
import numpy as np
import cv2

rc_car_cascade10 = cv2.CascadeClassifier('rc_car_cascade10.xml')

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # add this
    # image, reject levels level weights.
    rc_cars = rc_car_cascade10.detectMultiScale(gray, 50, 50)
    
    # add this
    for (x,y,w,h) in rc_cars:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)

        
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()