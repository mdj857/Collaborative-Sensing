'''
This class drives the object tracker trained by the OpenCV library.
To do this, the .xml file returned by model training is used as a 
Cascade classifier an attribute of the classifier
and rectangular boxes are drawn around the predicted
region(s) of interest. The center of masses of each prediction are recorded for each image frame. 
the predicted center of mass is given by (x, y) aand these are stashed in the predicted_preds attribute

Created by Matthew Johnson 09/17/18 
'''

import numpy as np
import cv2

class PlanetDetector:

    def __init__(self, model):
        self.model = model
        self.previous_preds = []
	self.prevX = []
	self.prevY = []
        self.classifier = cv2.CascadeClassifier(self.model)
        #cap = cv2.VideoCapture(0)
        gst_str = ("v4l2src device=/dev/video{} ! "
                       "video/x-raw, width=(int){}, height=(int){}, format=(string)RGB ! "
                       "videoconvert ! appsink").format(1, 1280, 720)
        self.cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

    def runCascadeClassifier(self):
        ret, img = self.cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = gray[40:-40, 0:-1]
	s_img = cv2.resize(img, (0,0), fx=0.75, fy=0.75)
	s_gray = cv2.resize(gray, (0,0), fx = 0.75, fy = 0.75)
	

	font                   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (10,500)
	fontScale              = 1
	fontColor              = (255,255,255)
	lineType               = 2

        # add this
        # image, reject levels level weights.
        planets = self.classifier.detectMultiScale(s_img, 25, 50)
	if(len(planets) != 0):	  
          (x,y,w,h) = planets[0]
          roi_gray = s_gray[y:y+h, x:x+w]
          roi_color = s_img[y:y+h, x:x+w]
	  #print(str(np.mean(roi_gray)))
	  i=0
	  while(np.mean(roi_gray) >= 2500):
	    if(i < len(planets) - 1):
	      i+=1
	      (x,y,w,h) = planets[i]
              roi_gray = s_gray[y:y+h, x:x+w]
              roi_color = s_img[y:y+h, x:x+w]
	      
	    else:
	        cv2.imshow('s_img',s_img)
		k = cv2.waitKey(30) & 0xff
	        return
         #for (x,y,w,h) in planets:
          # only get first planet, add the prediction to the the queue
          #x,y,w,h = planets.pop(0)
	  cv2.putText(s_img,str(np.mean(roi_gray)), 
                (x,y), 
                font, 
                fontScale,
                fontColor,
                lineType)
	  cv2.rectangle(s_img,(x,y),(x+w,y+h),(255,255,0),2)
	  center_of_mass = (x + w/2, y + h/2)
	  self.previous_preds.append(center_of_mass)
	  # only keep first two
	  if(len(self.previous_preds) > 2):
	    self.previous_preds.pop(0) 
	  #print self.previous_preds + '\n'
	
	  

        cv2.imshow('s_img',s_img)
        k = cv2.waitKey(30) & 0xff
        #if k == 27:
        #    break

        

    def get_last_two_preds(self):
        return self.previous_preds

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
