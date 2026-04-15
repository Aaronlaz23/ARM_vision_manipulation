import cv2 as cv
import os
import matplotlib
import numpy as np
matplotlib.use("Agg")
from PIL import Image
from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode, ZBarSymbol

os.system("rpicam-still -o ../images/qrimg.jpg --width 1920 --height 1080")
img = Image.open("../images/qrimg.jpg")
cvimage = np.array(img)
cvimage = cv.cvtColor(cvimage, cv.COLOR_RGB2GRAY)
img = Image.fromarray(cvimage)

if img is None:
        print("IMG not found")
else:
	print("Image WAS found Succesfully")

qrlist = decode(cvimage)

for qr in qrlist:
	rect = qr.rect
	cv.rectangle(cvimage, (rect.left, rect.top), (rect.left +  rect.width, rect.top + rect.height), (0, 255, 255), 2)

if not qrlist:
	print("NO QR ON IMAGE")
else:
	cv.imwrite("../images/qrimgdetected.jpg", cvimage)


