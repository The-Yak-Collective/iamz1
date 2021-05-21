import cv2
import numpy as np
from matplotlib import pyplot as plt

cam = cv2.VideoCapture(0)

cv2.namedWindow("test-st")

img_counter = 0

imgL = cv2.imread("opencv_frame_0.png",0)
imgR = cv2.imread("opencv_frame_1.png",0)
print("to here")
stereo = cv2.StereoBM_create(numDisparities=32, blockSize=7)
print("now here")
disparity = stereo.compute(imgL,imgR)
print("and finally")
cv2.imwrite("disp_img.png", disparity)
cv2.destroyAllWindows()