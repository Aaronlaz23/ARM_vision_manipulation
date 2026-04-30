#Square detection by - Eamorr modified by comunity
#Detection and location by Aaron23

import cv2 as cv
import os
import matplotlib
import numpy as np
matplotlib.use("Agg")
from PIL import Image
from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode, ZBarSymbol

redsfound = False
blackfound = False
loopcount = 0

while (not redsfound or not blackfound) and loopcount < 20:
	redsfound = False
	blackfound = False
	loopcount = loopcount + 1
	print(f"\n Current Loop {loopcount}")

	os.system("rpicam-still --immediate -o ../images/sqimg.jpg --width 640 --height 480")
	image = Image.open("../images/sqimg.jpg")
	frame = np.array(image)
	img = cv.GaussianBlur(frame, (5, 5), 0)

	img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

	lower = np.array([0, 0, 0], np.uint8)
	upper = np.array([180, 255, 50], np.uint8)
	separated = cv.inRange(img, lower, upper)

	rlower = np.array([100, 50, 120], np.uint8)
	rupper = np.array([130, 255, 255], np.uint8)
	rseparated = cv.inRange(img, rlower, rupper)

	bimage = frame

	# Detect square, identify and save position
	contours, hierarchy = cv.findContours(separated, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
	max_area = 0
	largest = None
	location = None
	blocation = None
	for idx, contour in enumerate(contours):
		area = cv.contourArea(contour);
		if area > max_area:
			max_area = area
			largest = contour
			if largest is not None:
				moment = cv.moments(largest)
				if moment["m00"] > 1000:
					rect = cv.minAreaRect(largest)
					rect = ((rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), rect[2])
					(width, height) = (rect[1][0], rect[1][1])
					location = rect
					box = cv.boxPoints(rect)
					box = box.astype(int)
					if (height > 0.8 * width and height < 1.2 * width):
						newimg = cv.drawContours(bimage, [box], 0, (0, 0, 255), 2)
						center, size, angle = location
						center = (float(round(center[0])), float(round(center[1])))
						blocation = center
						cv.putText(newimg, f"({center[0]},{center[1]})", (int(center[0]), int(center[1])), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
						cv.imwrite("../images/sqimgdetected.jpg", newimg)
						print("\n Square :) -------------------------------------\n")
						blackfound = True

	redimg = frame
	rcount = 0

	# Detect two squares
	rcontours, rhierarchy = cv.findContours(rseparated, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
	rlocation1 = None
	rlocation2 = None
	for idx, rcontour in enumerate(rcontours):
		area = cv.contourArea(rcontour);
		if rcontour is not None:
			moment = cv.moments(rcontour)
			if moment["m00"] > 1000:
				rrect = cv.minAreaRect(rcontour)
				rrect = ((rrect[0][0], rrect[0][1]), (rrect[1][0], rrect[1][1]), rrect[2])
				(width, height) = (rrect[1][0], rrect[1][1])
				rlocation = rrect
				box = cv.boxPoints(rrect)
				box = box.astype(int)
				if (height > 0.8 * width and height < 1.2 * width):
					cv.drawContours(redimg, [box], 0, (0, 0, 255), 2)
					rcount = rcount + 1
					center, size, angle = rlocation
					center = (float(round(center[0])), float(round(center[1])))
					if (rcount == 1):
						rlocation1 = center
					if (rcount == 2):
						rlocation2 = center
					cv.putText(redimg, f"({center[0]},{center[1]})", (int(center[0]), int(center[1])), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
					print(f"\n RedSquare: {rcount} Location {center} \n")

	if (rcount == 2):
		redsfound = True
		cv.imwrite("../images/redimg.jpg", redimg)

if (blocation is not None and rcount == 2):
	difference = (rlocation1[0] - rlocation2[0], rlocation1[1] - rlocation2[1])
	if (difference[1] == 0):
		difference[1] = 1
	blocation = ((blocation[0] - rlocation2[0])*(150/difference[0]), (blocation[1] - rlocation2[1])*(150/difference[1]))
	print(f"\n the current location of b is: {blocation}, difference is {difference}\n")
	Xhex = hex(150 - int(blocation[0]))
	Yhex = hex(int(blocation[1]))
	Ohex = hex(1)
	os.system("sudo i2cdetect -y 1")
	os.system(f"sudo i2ctransfer -y 1 w3@0x0a {Xhex} {Yhex} {Ohex}")
