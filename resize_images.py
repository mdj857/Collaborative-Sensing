'''
This file resizes all files in the /img directory to a 50x50 and grayscles the images
'''

import os
import cv2

def clean():
	for directory in os.walk():
		for filename in os.listdir(directory):
			img = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
			resized_image = cv2.resize(img, (100, 100))
			cv2.imwrite(filename+".jpg",resized_image)
clean()