'''
This file drives the object tracker trained by the OpenCV library.
To do this, the .xml file returned by model training is used as a 
Cascade classifier and rectangular boxes are drawn around the predicted
region(s) of interest.

Created by Matthew Johnson 09/17/18 
'''
import numpy as np
import cv2


rc_car_cascade10 = cv2.CascadeClassifier('/home/nvidia/OpenCV/Collaborative-Sensing/old_models/model_4/cascade.xml')
#rc_car_cascade10 = cv2.CascadeClassifier('/home/nvidia/OpenCV/Collaborative-Sensing/model/cascade.xml')
#cap = cv2.VideoCapture(0)
gst_str = ("v4l2src device=/dev/video{} ! "
               "video/x-raw, width=(int){}, height=(int){}, format=(string)RGB ! "
               "videoconvert ! appsink").format(1, 1280, 720)
cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
imNo = 0

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (128,128,128)
lineType               = 2



while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = equalizeHist(gray)

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,500)
    fontScale              = 1
    fontColor              = (128,128,128)
    bFontColor             = (255,0,0)
    gFontColor             = (0,255,0)
    rFontColor             = (0,0,255)
    lineType               = 2

    small_i = cv2.resize(img, (0,0), fx=0.75, fy=0.75)
    small = cv2.resize(gray, (0,0), fx=0.75, fy=0.75) 
    
    found = False
    # add this
    # image, reject levels level weights.
    rc_cars = rc_car_cascade10.detectMultiScale(small, scaleFactor=50, minNeighbors=50)
    
    # add this
    i=0

    for (x,y,w,h) in rc_cars:
        roi_gray = small[y:y+h, x:x+w]
        roi_color = small_i[y:y+h, x:x+w]
        roi_b = small_i[y:y+h, x:x+w, 0]
        roi_g = small_i[y:y+h, x:x+w, 1]
        roi_r = small_i[y:y+h, x:x+w, 2]
        if(np.mean(roi_gray) < 100 and np.mean(roi_r) < np.mean(roi_g)):
          i += 1
          if(i>0 and i<10):
		  if(i == 1):
		    #found = True
		    cv2.rectangle(small_i,(x,y),(x+w,y+h),(0,255,0),2)
		  else:
		    cv2.rectangle(small_i,(x,y),(x+w,y+h),(0,0,255),2)
		  cv2.putText(small_i,str(int(np.mean(roi_gray))), 
		    (x,y), 
		    font, 
		    fontScale,
		    fontColor,
		    lineType)
		  cv2.putText(small_i,str(int(np.mean(roi_b))), 
		    (x,y-75), 
		    font, 
		    fontScale,
		    bFontColor,
		    lineType)
		  cv2.putText(small_i,str(int(np.mean(roi_g))), 
		    (x,y-50), 
		    font, 
		    fontScale,
		    gFontColor,
		    lineType)
		  cv2.putText(small_i,str(int(np.mean(roi_r))), 
		    (x,y-25), 
		    font, 
		    fontScale,
		    rFontColor,
		    lineType) 
		  roi_gray = gray[y:y+h, x:x+w]
		  roi_color = small[y:y+h, x:x+w]
    if(found):
      if(imNo < 100):
        cv2.imwrite('../image_testing/'+str(imNo)+'.png', small_i)
        imNo+=1
        print(str(imNo))
      else:
        exit(0)
    cv2.imshow('small_i',small_i)
    
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
