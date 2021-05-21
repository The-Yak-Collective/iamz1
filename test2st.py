import cv2
import numpy as np
from matplotlib import pyplot as plt
import time



img_counter = 0

imgL = cv2.imread("opencv_frame_0.png",0)
imgR = cv2.imread("opencv_frame_1.png",0)


stereo = cv2.StereoSGBM_create(numDisparities=64, blockSize=5)

start = time.time()

disparity = stereo.compute(imgL,imgR)


end = time.time()
print(end - start)
cv2.imwrite("disp_img.png", disparity)
