import cv2 as cv
import matplotlib
matplotlib.use("Agg")
from PIL import Image
from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode, ZBarSymbol

img = cv.imread("../images/recognize_stop_sign/image.jpg")

if img is None:
	print("IMG not found")

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
stop_cascade = cv.CascadeClassifier("../images/recognize_stop_sign/stop_data.xml")

found = stop_cascade.detectMultiScale(img_gray, minSize=(20, 20))
for (x, y, w, h) in found:
    cv.rectangle(img_gray, (x, y), (x + w, y + h), (0, 255, 0), 5)

plt.imshow(img_gray)
plt.savefig("../images/graph.jpg", dpi = 300)
plt.close()

