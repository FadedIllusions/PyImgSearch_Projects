# Import Needed Packages
import numpy as np
import cv2


def order_points(pts):
	# Init Coordinate List That Will Be Ordered Such That The First Entry
	# Is The Top-Left, The Second Is The Top-Right, The Third Is The
	# Bottom-Right, And The Fourth Is The Bottom-Left
	rect = np.zeros((4,2), dtype = "float32")
	
	# Top-Left Point Will Have Smallest Sum, Whereas The Bottom-Right
	# Will Have The Largest Sum
	s = pts.sum(axis=1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	
	# Compute Difference Between Points, The Top-Right Point Will Have The
	# Smallest Difference; Whereas, The Bottom-Left Will Have The Largest
	diff = np.diff(pts, axis=1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	
	# Return Order Coords
	return rect


def four_point_transform(image, pts):
	# Obtain Consistent Order Of Points And Unpack Individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	
	# Computer Width Of Image, Which Will Be Max Distance Between Bottom-Right
	# And Bottom-Left X-Coordinates Or Top-Right And Top-Left X-Coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	
	# Compute Height Of Image, Which Will Be Max Distance Between Top-Right
	# And Bottom-Right X-Coordinates Or Top-Left And Bottom-Left Coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	
	# After Obtaining Dimensions, Construct Set Of Destination Points To
	# Obtain "Bird's Eye View", (I.E., Top-Down View) Of Image, Specifying
	# Points In TL, TR, BR, BL Order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 2, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	
	# Compute Perspective Transform Matrix And Apply
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	
	# Return Warped Image
	return warped


