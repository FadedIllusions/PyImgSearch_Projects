This project is from [*Adrian's*](https://github.com/jrosebr1/) blog post [*"How to Build a Kick-Ass Mobile Document Scanner in Just 5 Minutes"*](https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/) in extension to his post [*"4 Point OpenCV getPerspective Transform Example"*](https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/).

The project uses OpenCV's findContours(), getPerspectiveTransform(), and warpPerspective() to create an outline for an OpenCV-based 'mobile' document scanner.

<code>$ python scan.py --image images/receipt.jpg</code>
![Document Scanner Screenshot](docs/images/scanner_screenshot.png?raw=true)
