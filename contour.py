from imutils import paths

import numpy as np
import cv2 as cv
import cv2
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to images directory")
args = vars(ap.parse_args())
 

for imagePath in paths.list_images(args["images"]):
    # load the image and resize it to (1) reduce detection time
    # and (2) improve detection accuracy
    im = cv2.imread(imagePath)
    orig = im.copy()
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)

    
    im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # show some information on the number of bounding boxes
    filename = imagePath[imagePath.rfind("/") + 1:]

    cv2.imshow("Before NMS", orig)
    cv2.imshow("After NMS", im)
    
    if(cv2.waitKey(1)& 0xFF==ord('q')):
            break
    cv2.waitKey(0)