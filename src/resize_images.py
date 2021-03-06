'''
This file resizes all files in the /img directory to a 50x50 and grayscles the images
'''

import os
import cv2

def clean():
  f = open("info.lst", "w+")
  for filename in os.listdir('.'):
    if(not 'resize' in filename):
      img = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
      if(img is not None):
        #resized_image = cv2.resize(img, (50, 50))
        newFile = filename.split(".")[0] + ".png"
        f.write("\npos/" + newFile + " 1 0 0 " + str(img.shape[1])  + " " + str(img.shape[0]))
        cv2.imwrite(newFile,img)
  f.close()
clean()
