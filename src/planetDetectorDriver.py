from planetDetector import *
import time
detector = PlanetDetector('/home/nvidia/OpenCV/Collaborative-Sensing/old_models/model_4/cascade.xml')
#detector = PlanetDetector('/home/nvidia/OpenCV/Collaborative-Sensing/model/cascade.xml')
while 1:
	detector.runCascadeClassifier()
	print detector.get_last_measurement()
	#time.sleep(1)



