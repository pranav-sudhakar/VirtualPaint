# Virtual Paint

A Python + OpenCV app that lets you draw on your webcam feed using any blue
object, like a pen with a blue cap. No touchscreen or special hardware needed.

## How it works

1. The webcam frame is converted from BGR to HSV color space.
2. A color mask isolates blue pixels (`cv2.inRange`).
3. The mask is dilated and its contours are found.
4. The center of the minimum enclosing circle of the detected blob is calculated.
5. That center point is drawn onto the live feed, tracing your movement.

## Features

- Real-time blue object tracking
- On-screen palette: switch between **blue**, **green** and **red** by moving
  the pen over a color box
- **Clear** button to wipe the canvas
- Separate windows showing the mask and the detected color for debugging
