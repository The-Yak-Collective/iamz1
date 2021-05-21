import cv2
import numpy as np
from matplotlib import pyplot as plt

cam = cv2.VideoCapture(0)

cv2.namedWindow("test-st")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()


imgL = cv2.imread("opencv_frame_0.png",0)
imgR = cv2.imread("opencv_frame_1.png",0)
print("to here")
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
print("now here")
disparity = stereo.compute(imgL,imgR)
print("and finally")
cv2.imwrite("disp_img.png", disparity)
cv2.destroyAllWindows()