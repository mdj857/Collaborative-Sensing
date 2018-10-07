import planetDetector

detector = planetDetector('model\cascade.xml')
while 1:
	detector.runCascadeClassifier()
	print detector.get_last_two_preds()



