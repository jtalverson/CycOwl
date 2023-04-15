import jetson_inference 
import jetson_utils
import os

from imutils import paths
import imutils
import numpy as np
import cv2

objectWidths = {}

with open("./objectWidths.txt") as allWidths:
        widths = allWidths.readlines()
        for width in widths:
                currentSplit = width.split(',')
                speechWarnings[currentSplit[0]] = currentSplit[1].strip()

print (objectWidths)

def find_marker(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key=cv2.contourArea)
	return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
	return (knownWidth * focalLength) / perWidth

KNOWN_DISTANCE = 24.0
KNOWN_WIDTH = 8.0
image = cv2.imread("image path")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

print (focalLength)

# inches = distance_to_camera(KNOWN_WIDTH, focalLength, (BASE_WIDTH / NEW_WIDTH) * boxWidth)



net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson_utils.gstCamera(1280, 720, "/dev/video1")
display = jetson.utils.glDisplay()



while display.IsOpen():
	img, width, height = camera.CaptureRGBA()
	detections = net.Detect(img, width, height)
	display.RenderOnce(img, width, height)
	display.SetTitle("Object Detection | Network: {:0f} FPD+S".format(net.GetNetworkFPS()))

	for detection in detections:
		print(net.GetClassDesc(detection.ClassID))
		print(detection.Width)
		os.system("mpg321 " + filepath + net.GetClassDesc(detection.ClassID) + ".mp3")
