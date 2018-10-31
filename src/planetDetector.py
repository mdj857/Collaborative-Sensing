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
import pickle
import cv2

def planetFilter(planets, height):
	i=0

	for (x,y,w,h) in planets:
		i+=1
		if(i>0 and i<5 and y < height/3):
			planet = x, y, w, h
			return planet
	return None

class PlanetDetector:
    def __init__(self, model, Test, Eval):
        self.model = model
        self.Test = Test
        self.Eval = Eval
        self.imNo = 0
        # self.previous_preds = []
        # self.prevX = []
        # self.prevY = []
        self.last_measurement = []
        self.classifier = cv2.CascadeClassifier(self.model)
        # self.cap = cv2.VideoCapture(0)
        gst_str = ("v4l2src device=/dev/video{} ! "
                   "video/x-raw, width=(int){}, height=(int){}, format=(string)RGB ! "
                   "videoconvert ! appsink").format(1, 1280, 720)
        self.cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

    def runCascadeClassifier(self):
        ret, img = self.cap.read()
        #cv2.rectangle(img, (440, 150), (750, 460), (0, 255, 255), 2)
        #sun_img = img[390:710, 140:460]
        #sun_b = sun_img[0:150, 0:150, 0]
        #sun_r = sun_img[0:150, 0:150, 1]
        #sun_g = sun_img[0:150, 0:150, 2]
        #
        #print(np.mean(sun_b))
        #print(np.mean(sun_r))
        #print(np.mean(sun_g))
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = gray[40:-40, 0:-1]
        s_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        s_gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
	
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        fontColor = (128, 128, 128)
        bFontColor = (255, 0, 0)
        rFontColor = (0, 255, 0)
        gFontColor = (0, 0, 255)
        lineType = 2

        # add this
        # image, reject levels level weights.
        planets = self.classifier.detectMultiScale(s_gray, 15, 50)
        earth = planetFilter(planets, s_gray.shape[0])
        if (earth is not None):
            (x, y, w, h) = earth
            roi_gray = s_gray[y:y + h, x:x + w]
            roi_color = s_img[y:y + h, x:x + w]
            roi_b = s_img[y:y + h, x:x + w, 0]
            roi_r = s_img[y:y + h, x:x + w, 1]
            roi_g = s_img[y:y + h, x:x + w, 2]
            if (self.Test):
                cv2.putText(s_img, str(int(np.mean(roi_gray))),
                            (x, y),
                            font,
                            fontScale,
                            fontColor,
                            lineType)
                cv2.putText(s_img, str(int(np.mean(roi_b))),
                            (x, y - 75),
                            font,
                            fontScale,
                            bFontColor,
                            lineType)
                cv2.putText(s_img, str(int(np.mean(roi_r))),
                            (x, y - 50),
                            font,
                            fontScale,
                            rFontColor,
                            lineType)
                cv2.putText(s_img, str(int(np.mean(roi_g))),
                            (x, y - 25),
                            font,
                            fontScale,
                            gFontColor,
                            lineType)
            cv2.rectangle(s_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center_of_mass = (x + w / 2, y + h / 2)
            self.last_measurement.append(center_of_mass)
            # only keep first two
            if (len(self.last_measurement) > 2):
                self.last_measurement.pop(0)
            if (self.Eval):
                if (self.imNo < 100):
                    print(str(cv2.imwrite('../image_testing/' + str(self.imNo) + '.png', s_img)))
                    self.imNo += 1
                else:
                	print("")
                    #exit(1)
		
        cv2.imshow('Output', cv2.resize(s_img, (0, 0), fx=2., fy=2.))
        k = cv2.waitKey(10) & 0xff
        if k == 27:
        	exit(0)

    def calculateR(self, x, y, sunX, sunY):
        #return np.sqrt((x - sunX) ** 2 + (y - sunY) ** 2)
        return x-sunX

    def get_last_measurement(self):
        if (len(self.last_measurement) > 0):
            x = self.last_measurement[0][0]
            y = self.last_measurement[0][1]
            # TODO: change 0,0 with sun x and y coordinates
            r = self.calculateR(x, y, 295, 153)
            return r
        else:
            return 0

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
