from planetDetector import *
import time

detector = PlanetDetector('/home/nvidia/OpenCV/Collaborative-Sensing/model/cascade.xml')
while 1:
	detector.runCascadeClassifier()
	print detector.get_last_two_preds()
	#time.sleep(1)



