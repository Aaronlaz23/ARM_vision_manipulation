import cv2
import os
import matplotlib
import numpy as np
matplotlib.use("Agg")
from PIL import Image
from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode, ZBarSymbol

os.system("rpicam-still -o ../images/qrimg.jpg --width 640 --height 480")
image = Image.open("../images/qrimg.jpg")

# Square Detection by - https://stackoverflow.com/q/17883023
# Position and interaction by Aaron23

frame=np.array(image)
img=cv2.GaussianBlur(frame, (5,5), 0)

img=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

lower=np.array([0, 0, 0],np.uint8)
upper=np.array([180, 255, 50],np.uint8)
separated=cv2.inRange(img,lower,upper)

#this bit draws a red rectangle around the detected region
contours,hierarchy=cv2.findContours(separated,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
max_area = 0
largest_contour = None
square_location = None
for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            largest_contour=contour
            if largest_contour is not None:
                moment = cv2.moments(largest_contour)
                if moment["m00"] > 1000:
                    rect = cv2.minAreaRect(largest_contour)
                    rect = ((rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), rect[2])
                    (width,height)=(rect[1][0],rect[1][1])
                    square_location = rect
                    print (f"{width} {height}")
                    box = cv2.boxPoints(rect)
                    box = box.astype(int)
                    if(height>0.9*width and height<1.1*width):
                            newimg = cv2.drawContours(frame,[box], 0, (0, 0, 255), 2)
                            cv2.imwrite("../images/imgnew.jpg", newimg)
                            print("SQUARE :) \n")


center, size, angle = square_location
center = (float(round(center[0])), float(round(center[1])))
print(f"center {center} ")
cv2.putText(img,  f"({center[0]}, {center[1]})", (int(center[0]), int(center[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.imwrite("../images/located.jpg", img)
