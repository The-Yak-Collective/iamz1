import cv2
import sys

cam = cv2.VideoCapture('/dev/video2')

img_name = "a_snap.png"
if len(sys.argv)>1:
    img_name=argv[1]

ret, frame = cam.read()
if not ret:
    print("failed to grab frame")
else:
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))

cam.release()

