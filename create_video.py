import numpy as np
import cv2
import cv2.cv as cv
import glob

files = glob.iglob('*.png')

if __name__ == '__main__':
    while True:
        try:
            img = cv.LoadImage(files.next())
        except StopIteration:
            print "Stopping"
            break
        cv.ShowImage('bom',img)
        if cv2.waitKey(5) == 27:
            break

