import cv2
import numpy as np
import sys
import time
import collections
from collections import deque
from numpy.testing._private.utils import break_cycles

print('starting video capture')
vid = cv2.VideoCapture(0)
ret, frames = vid.read() 

positions = []
red_positions = []
blue_positions = []
green_positions = []

color_stat = (0,0,255)

if ret is True:
    print("File Loaded Successfully...")
    time.sleep(1)
else:
    sys.exit("Failed to load file, try again")

def find_color(color_s):
    if color_s == (0,0,255):
        return "red"
    if color_s == (0,255,0):
        return "green"
    if color_s == (255,0,0):
        return "blue"

while True:
    ret, frames = vid.read()
    frames = cv2.resize(frames, (1920,1080))
    frames = cv2.flip(frames, 1)

    kernel = np.ones((5,5), np.uint8)
    hsv = cv2.cvtColor(frames, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    color_detected = cv2.bitwise_and(frames, frames, mask=mask)

    vid_dilation = cv2.dilate(color_detected, kernel, iterations=3)

    gray = cv2.cvtColor(vid_dilation, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50,200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.rectangle(frames, (25,25), (400, 200), (255,0,0), -1)
    cv2.rectangle(frames, (425,25), (800,200), (0,255,0), -1)
    cv2.rectangle(frames, (825,25), (1200,200), (0,0,255), -1)
    cv2.rectangle(frames, (1450,25), (1825,200), (112,112,112), -1)
    cv2.putText(frames, "Blue", (400-250,200-78), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 5, cv2.LINE_AA)
    cv2.putText(frames, "Green",(800-290,142-15), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 5, cv2.LINE_AA)
    cv2.putText(frames, "Red", (1200-250, 200-78), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 5, cv2.LINE_AA)
    cv2.putText(frames, "Clear", (1825-290, 142-15), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 5, cv2.LINE_AA)
    cv2.line(frames, (0,230), (2000,220), (236,234,1), 4)

    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        perimeter = int(perimeter)

        if perimeter > 400:
            #cv2.drawContours(frames, cnt, -1, (255,0,0), 2)
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))

            if center[1] < 200 and center[1] > 25 and center[0] > 25 and center[0] < 400:
                color_stat = (255,0,0)
            elif center[0] < 800 and center[0] > 425 and center[1] < 200 and center[1] > 25:
                color_stat = (0,255,0)
            elif center[0] < 1200 and center[0] > 825 and center[1] < 200 and center[1] > 25:
                color_stat = (0,0,255)
            elif center[0] < 1825 and center[0] > 1450 and center[1] < 200 and center[1] > 25:
                blue_positions = []
                green_positions = []
                red_positions = []
            
            color = find_color(color_stat)

            if color == "red":
                red_positions.append(center)
            if color == "blue":
                blue_positions.append(center)
            if color == "green":
                green_positions.append(center)

            for rpos in red_positions:
                cv2.circle(frames, rpos, 10, (0,0,255), -1)
            for bpos in blue_positions:
                cv2.circle(frames, bpos, 10, (255,0,0), -1)
            for gpos in green_positions:
                cv2.circle(frames, gpos, 10, (0,255,0), -1)

        else:
            for rpos in red_positions:
                cv2.circle(frames, rpos, 10, (0,0,255), -1)
            for bpos in blue_positions:
                cv2.circle(frames, bpos, 10, (255,0,0), -1)
            for gpos in green_positions:
                cv2.circle(frames, gpos, 10, (0,255,0), -1)

    cv2.imshow("mask",mask)
    cv2.imshow("detected_color",vid_dilation)
    cv2.imshow("frames",frames)

    if cv2.waitKey(1) == ord('q'):
        print("--ABORTED PROGRAM--")
        break
    else:
        pass    

vid.release()
cv2.destroyAllWindows()