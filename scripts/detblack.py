import cv2 as cv
import os
import matplotlib
import numpy as np
matplotlib.use("Agg")
from PIL import Image
from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode, ZBarSymbol

os.system("rpicam-still -o ../images/qrimg.jpg --width 640 --height 480")
image = Image.open("../images/qrimg.jpg")
img = np.array(image)

blur = cv.GaussianBlur(img, (5,5), 0)

# Convert to HSV
hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

# Black range
lower = np.array([0, 0, 0], np.uint8)
upper = np.array([180, 255, 50], np.uint8)

mask = cv.inRange(hsv, lower, upper)

# Find contours
contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

max_area = 0
largest_contour = None

# Find largest contour
for contour in contours:
    area = cv.contourArea(contour)
    if area > max_area:
        max_area = area
        largest_contour = contour

# Process largest contour
if largest_contour is not None:
    moment = cv.moments(largest_contour)

    if moment["m00"] > 1000:
        rect = cv.minAreaRect(largest_contour)

        (cx, cy), (width, height), angle = rect

        print(f"Width: {width}, Height: {height}")
        print(f"Center: ({cx}, {cy})")

        # Get box points (FIXED)
        box = cv.boxPoints(rect)
        box = box.astype(int)

        # Check square shape
        if height > 0.9 * width and height < 1.1 * width:
            newimg = cv.drawContours(img, [box], 0, (0, 0, 255), 2)
            cv.imwrite(newimg)
        else:
            print("NO square found")
            print("---\n")
