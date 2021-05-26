import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import sys



img_counter = 0

imgL = cv2.imread(sys.argv[1],0)
imgR = cv2.imread(sys.argv[2],0)


stereo = cv2.StereoSGBM_create(numDisparities=16, blockSize=11)

start = time.time()

disparity = stereo.compute(imgL,imgR)


end = time.time()
print(end - start)
cv2.imwrite("disp_img.png", disparity)
