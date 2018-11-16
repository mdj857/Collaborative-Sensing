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
  '/home/nvidia/OpenCV/Collaborative-Sensing/model/cascade.xml',
  1,
  Test,
  Eval)


measurements = []
i = 0
#detector = PlanetDetector('/home/nvidia/OpenCV/Collaborative-Sensing/model/cascade.xml')
while True:
	detector.runCascadeClassifier()
	i+=1
	print(str(detector.get_last_measurement()))
	#print(i)
	#time.sleep(0.05)
print("Done")


