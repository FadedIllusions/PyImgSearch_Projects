# Import Needed Packages
import numpy as np
import cv2


def color_transfer(source, target, clip=True, preserve_paper=True):
	"""
	Transfers The Color Distribution From The Source To Target Image
	Using Mean And Standard Deviations Of The LAB Color Space.
	
	This Implementation, Written By Adrian Rosebrock,
	(http://www.pyimagesearch.com), Is (Loosely) Based On The "Color
	Transfer Between Images" Paper By Reinhard Et El., 2001
	
	Parameters:
	-----------
	source: NumPy Array
		OpenCV Image In BGR Color Space (The Source Image)
	
	target: NumPy Array
		OpenCV Image In BGR Color Space (The Target Image)
	
	clip:
		Should Components Of LAB Image Be Scaled By np.clip Before
		Converting Back To BGR Color Space?
		
		If False, Components Will Be Min-Max Scaled Appropriately.
		Clipping Will Keep Target Image Brightness Truer To The Input.
		Scaling Will Adjust Image Brightness To Avoid Washed-Out Portions
		In The Resulting Color Transfer That Can Be Caused By Clipping.
	preserve_paper:
		Should Color Transfer Strictly Follow Methodology Laid Out In
		Original Paper? The Method Does Not Always Produce Aesthetically
		Pleasing Results.
		
		If False, LAB Components Will Be Scaled Using Reciprocal Of The
		Scaling Factor Proposed In Paper. This Method Seems To Produce
		More Consistently Aesthetically Pleasing Results
		
	Returns:
	--------
	transfer: NumPy Array
		OpenCV Image (w, h, 3) NumPy Array (uint8)
	"""
	

	# Conver Images From BGR To LAB Color Space, Being Certain To Utilize The
	# Floating Point Data Type. (Note: OpenCV Expects Floats To Be 32-Bit, Use
	# Instead Of 64-Bit
	source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
	target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")
	
	# Compute Color Statistics For Source And Target Images
	(lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source)
	(lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_stats(target)
	
	# Subtract Means From Target Image
	(l, a, b) = cv2.split(target)
	l -= lMeanTar
	a -= aMeanTar
	b -= bMeanTar
	
	if preserve_paper:
		# Scale By Standard Deviations Using Paper Proposed Factor
		l = (lStdTar / lStdSrc) * l
		a = (aStdTar / aStdSrc) * a
		b = (bStdTar / bStdSrc) * b
	else:
		# Scale By Std Deviations Using Reciprocal Of Paper Proposed Factor
		l = (lStdSrc / lStdTar) * l
		a = (aStdSrc / aStdTar) * a
		b = (bStdSrc / bStdTar) * b
		
	# Add Source Mean
	l += lMeanSrc
	a += aMeanSrc
	b += bMeanSrc
	
	# Clip/Scale Px Intensities [0,255] If Outside Such A Range
	l = _scale_array(l, clip=clip)
	a = _scale_array(a, clip=clip)
	b = _scale_array(b, clip=clip)
	
	# Merge Chans ANd Convert Back To BGR Color Space, Utilizing 8-Bit Unsigned
	# Integer Data Type
	transfer = cv2.merge([l, a, b])
	transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)
	
	# Return Color-Transferred Image
	return transfer


def image_stats(image):
	"""
	Parameters:
	-----------
	image: NumPy Array
		OpenCV Image In LAB Color Space
		
	Returns:
	--------
		Tuple Of Mean And Standard Deviations For L, A, B Channels, respectively
	"""
	
	# Compute Mean And Std Deviation Of Each Channel
	(l, a, b) = cv2.split(image)
	(lMean, lStd) = (l.mean(), l.std())
	(aMean, aStd) = (a.mean(), a.std())
	(bMean, bStd) = (b.mean(), b.std())
	
	# Return Color Statistics
	return(lMean, lStd, aMean, aStd, bMean, bStd)



def _min_max_scale(arr, new_range=(0,255)):
	"""
	Perform Min-Max Scaling To NumPy Array
	
	Parameters:
	-----------
	arr:
		NumPy Array To Be Scaled To [new_min, new_max] Range
	
	new_range:
		Tuple Of Form (min, max) Specifying Range Of Transformed Array
		
	Returns:
	--------
	NumPy Array That Has Been Scaled To Be In [new_range[0], new_range[1]] Range
	"""
	
	# Get Array's Current Min And Max
	mn = arr.min()
	mx = arr.max()
	
	# Check If Scaling Is Needed
	if mn < new_range[0] or mx > new_range[1]:
		# Perform Min-Max Scaling
		scaled = (new_range[1] - new_range[0]) * (arr - mn) / (mx - mn) + new_range[0]
	else:
		# Return Array If Already In Range
		scaled = arr
		
	return scaled

def _scale_array(arr, clip=True):
	"""
	Trim NumPy Array Values To [0,255] Range With Option Of Clipping Or Scaling.
	
	Parameters:
	-----------
	arr:
		Array To Be Trimmed To [0,255] Range
	
	clip:
		Should Array Be Scaled By np.clip? If False, Input Array Will Be Min-Max Scaled
		To Range [max([arr.min(), 0]), min([arr.max(), 255])]
		
	Returns:
	--------
		Scaled NumPy Array In Range [0,255]
	"""
	
	if clip:
		scaled = np.clip(arr, 0, 255)
	else:
		scale_range = (max([arr.min(), 0]), min([arr.max(), 255]))
		scaled = _min_max_scale(arr, new_range=scale_range)
		
	return scaled