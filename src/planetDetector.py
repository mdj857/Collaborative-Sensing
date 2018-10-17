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

    def __init__(self, model, Test, Eval):
        self.model = model
	self.Test = Test
	self.Eval = Eval
	self.imNo = 0
        #self.previous_preds = []
	#self.prevX = []
	#self.prevY = []
	self.last_measurement = []
        self.classifier = cv2.CascadeClassifier(self.model)
        #self.cap = cv2.VideoCapture(0)
        gst_str = ("v4l2src device=/dev/video{} ! "
                       "video/x-raw, width=(int){}, height=(int){}, format=(string)RGB ! "
                       "videoconvert ! appsink").format(1, 1280, 720)
        self.cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

    def runCascadeClassifier(self):
        ret, img = self.cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #gray = gray[40:-40, 0:-1]
	s_img = cv2.resize(img, (0,0), fx=0.75, fy=0.75)
	s_gray = cv2.resize(gray, (0,0), fx = 0.75, fy = 0.75)
	

	font                   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (10,500)
	fontScale              = 1
	fontColor              = (128,128,128)
	bFontColor             = (255,0,0)
	rFontColor             = (0,255,0)
	gFontColor             = (0,0,255)
	lineType               = 2

        # add this
        # image, reject levels level weights.
        planets = self.classifier.detectMultiScale(s_img, 25, 50)
	if(len(planets) != 0):	  
          (x,y,w,h) = planets[0]
          roi_gray = s_gray[y:y+h, x:x+w]
          roi_color = s_img[y:y+h, x:x+w]
          roi_b = s_img[y:y+h, x:x+w, 0]
          roi_r = s_img[y:y+h, x:x+w, 1]
          roi_g = s_img[y:y+h, x:x+w, 2]
	  i=0
	  while(np.mean(roi_gray) >= 75 or np.mean(roi_r) < np.mean(roi_g)):
	    if(i < len(planets) - 1):
	      i+=1
	      (x,y,w,h) = planets[i]
              roi_gray = s_gray[y:y+h, x:x+w]
              roi_color = s_img[y:y+h, x:x+w]
              roi_b = s_img[y:y+h, x:x+w, 0]
              roi_r = s_img[y:y+h, x:x+w, 1]
              roi_g = s_img[y:y+h, x:x+w, 2]
	      
	    else:
              cv2.imshow('s_img',s_img)
	      k = cv2.waitKey(30) & 0xff
	      return
	  if(self.Test):
		  cv2.putText(s_img,str(int(np.mean(roi_gray))), 
		        (x,y), 
		        font, 
		        fontScale,
		        fontColor,
		        lineType)
		  cv2.putText(s_img,str(int(np.mean(roi_b))), 
		        (x,y-75), 
		        font, 
		        fontScale,
		        bFontColor,
		        lineType)
		  cv2.putText(s_img,str(int(np.mean(roi_r))), 
		        (x,y-50), 
		        font, 
		        fontScale,
		        rFontColor,
		        lineType)
		  cv2.putText(s_img,str(int(np.mean(roi_g))), 
		        (x,y-25), 
		        font, 
		        fontScale,
		        gFontColor,
		        lineType)
	  cv2.rectangle(s_img,(x,y),(x+w,y+h),(255,255,0),2)
	  center_of_mass = (x + w/2, y + h/2)
	  self.last_measurement.append(center_of_mass)
	  # only keep first two
	  if(len(self.last_measurement) > 2):
	    self.last_measurement.pop(0)
	  if(self.Eval):
	    if(self.imNo < 100):
  	      print(str(cv2.imwrite('../image_testing/'+str(self.imNo)+'.png', s_img)))
              self.imNo+=1
            else:
              exit(1)
	
        cv2.imshow('s_img',s_img)
        k = cv2.waitKey(30) & 0xff
        #if k == 27:
        #    break

    def calculateR(self, x, y, sunX, sunY):
        return ((x-sunX)**2 + (y-sunY)**2)**(1/2)

    def get_last_measurement(self):
	if(len(self.last_measurement) > 0):
          x = self.last_measurement[0][0]
          y = self.last_measurement[0][1]
          # TODO: change 0,0 with sun x and y coordinates
          r = self.calculateR(x, y, 0, 0)
          return r
	else:
	  return 0

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
