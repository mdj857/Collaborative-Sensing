'''
This file resizes all files in the /img directory to a 50x50 and grayscles the images
'''

import os
import cv2

def clean():
  for filename in os.listdir('.'):
    if(not 'resize' in filename):
      img = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
      resized_image = cv2.resize(img, (100, 100))
      cv2.imwrite(filename,resized_image)
clean()
