# Usage:
# python scan.py --image images/receipt.jpg

# Import Needed Packages
from helpers.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import imutils
import cv2


# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path To Input Image")
args = vars(ap.parse_args())


# Load Image And Compute Ratio Of Old Height To New Height, Clone, Resize
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
original = image.copy()
image = imutils.resize(image, height=500)

# Conver Image To Grayscale, Blur, Find Edges
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(gray, 75, 200)
grayEdged = np.hstack((gray, edged))

# Display Original And Edged Images
print("[INFO] Step 001: Edge Detection...")
cv2.imshow("Step 001 -- Edges", grayEdged)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Find Contours In Edged Image, Keep Only Largest, Init Screen Contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

# Iterate Over Contours
for c in cnts:
	# Approximate Contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	
	# If Approximated Contour Has Four Points, Can Assume Screen Found
	if len(approx) == 4:
		screenCnt = approx
		break
		
# Display Contour (Outline) Of Paper
print("[INFO] Step 002: Find Contours...")
cv2.drawContours(image, [screenCnt], -1, (0,255,0), 2)
cv2.imshow("Step 002 -- Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Apply Four Point Transform
warped = four_point_transform(original, screenCnt.reshape(4,2) * ratio)

# Convert To Grayscale, Threshold
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset=10, method="gaussian")
warped = (warped > T).astype("uint8") * 255

# Display Original And Scanned Images
print("[INFO] Step 003: Apply Perspective Transform...")
cv2.imshow("Original", imutils.resize(original, height=650))
cv2.imshow("Scanned", imutils.resize(warped, height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()