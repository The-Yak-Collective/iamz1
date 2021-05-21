import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

start = time.time()

img_counter = 0

imgL = cv2.imread("opencv_frame_0.png",0)
imgR = cv2.imread("opencv_frame_1.png",0)
print("to here")
stereo = cv2.StereoBM_create(numDisparities=64, blockSize=11)
print("now here")
disparity = stereo.compute(imgL,imgR)
print("and finally")
cv2.imwrite("disp_img.png", disparity)
end = time.time()
print(end - start)