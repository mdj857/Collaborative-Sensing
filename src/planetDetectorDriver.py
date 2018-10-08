from planetDetector import *
import time

detector = PlanetDetector('/home/nvidia/OpenCV/Collaborative-Sensing/old_models/model_2/cascade.xml')
while 1:
	detector.runCascadeClassifier()
	print detector.get_last_two_preds()
	#time.sleep(1)



