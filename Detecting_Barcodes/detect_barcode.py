# Usage:
# python detect_barcode.py --image images/barcode_01.jpg
# python detect_barcode.py --image images/barcode_02.jpg
# ...
# python detect_barcode.py --image images/barcode_06.jpg

# Import Needed Packages
import numpy as np
import argparse
import imutils
import cv2


# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path To Image File")
args = vars(ap.parse_args())


# Load Image And Convert To Grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Compute Scharr Gradient Magnitude Representation Of Images In Both
# X And Y Direction
ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

# Subtract Y-Gradient From X-Gradient
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

# Blur And Threshold Image
blurred = cv2.blur(gradient, (9, 9))
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

# Construct Closing Kernel And Apply To Threshold Image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Perform Series Of Erosions And Dilations
closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)

# Find Contours In Threshold Image, Sort By Area, Keeping Largest
cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

# Compute Rotated Bounding Box Of Largest Contour
rect = cv2.minAreaRect(c)
box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
box = np.int0(box)

# Draw Bounding Box Around Detected Barcode And Display Image
cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
cv2.imshow("Barcode", image)
cv2.waitKey(0)
cv2.destroyAllWindows()