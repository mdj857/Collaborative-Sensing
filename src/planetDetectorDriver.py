from planetDetector import *
import time
import sys

if('t' in sys.argv or 'test' in sys.argv):
  Test = True
else:
  Test = False

if('e' in sys.argv or 'eval' in sys.argv):
  Eval = True
else:
  Eval = False

detector = PlanetDetector(
  '/home/nvidia/OpenCV/Collaborative-Sensing/old_models/model_4/cascade.xml',
  Test,
  Eval)

#detector = PlanetDetector('/home/nvidia/OpenCV/Collaborative-Sensing/model/cascade.xml')
while 1:
	detector.runCascadeClassifier()
	#print detector.imNo
	#time.sleep(1)



