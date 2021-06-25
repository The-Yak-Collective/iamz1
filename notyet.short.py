import cv2
import sys
img_name = "a_snap.png"
if len(sys.argv)>1:
    img_name=argv[1]

cam = cv2.VideoCapture(0)
ret, frame = cam.read()
if not ret:
    cam = cv2.VideoCapture('/dev/video2')
    ret, frame = cam.read()

if not ret:
    print("failed to grab frame")
else:
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))

cam.release()

