This project is from [*Adrian's*](https://github.com/jrosebr1/) blog post [*"Detecting Barcodes in Images with Python and OpenCV"*](https://www.pyimagesearch.com/2014/11/24/detecting-barcodes-images-python-opencv/).

The project uses OpenCV's Scharr Gradient Magnitude (Sobel), thresholding, and contours in attempts to locate a barcode within an image; then, bounds said barcode with a rectangle.

<code>$ python detect_barcode.py --image images/barcode_06.jpg</code>
![Document Scanner Screenshot](docs/images/barcodes.png?raw=true)

