# Usage:
# python example.py --source images/ocean_sunset.jpg --target images/ocean_day.jpg

# Import Needed Packages
from color_transfer import color_transfer
import numpy as np
import argparse
import cv2


def show_image(title, image, width=300):
	# Resize Image To Constant Width
	r = width / float(image.shape[1])
	dim = width, int(image.shape[0] * r)
	resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
	
	# Display Resized Image
	cv2.imshow(title, resized)
	
	
def str2bool(v):
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError("Boolean Value Expected")
		
		
# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True, help="Path To Source Image")
ap.add_argument("-t", "--target", required=True, help="Path To Target Image")
ap.add_argument("-c", "--clip", type=str2bool, default='t',
				help="Should np.clip Scale LAB Values Before Final Converstion To BGR?"
				"Appropriate Min-Max Scaling Used If False.")
ap.add_argument("-p", "--preservePaper", type=str2bool, default='t',
				help="Should Color Transfer Strictly Follow Original Paper?")
ap.add_argument("-o", "--output", help="Path To Output Image (Optional)")
args = vars(ap.parse_args())


# Load Images
source = cv2.imread(args["source"])
target = cv2.imread(args["target"])

# Transfer Color Distribution From Source To Taget Image
transfer = color_transfer(source, target, clip=args["clip"], preserve_paper=args["preservePaper"])

# Check If Output Image Should Be Stored
if args["output"] is not None:
	cv2.imwrite(args["output"], transfer)
	
# Display Images And Await Keypress
show_image("Source", source)
show_image("Target", target)
show_image("Transfer", transfer)
cv2.waitKey(0)