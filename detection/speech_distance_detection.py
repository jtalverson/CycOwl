#!/usr/bin/env python3.6

import jetson_inference 
import jetson_utils
import os
import subprocess
from imutils import paths
import imutils
import numpy as np
import cv2
import time
import getpass
import pexpect
import shelve

program_start = time.time()
frames_processed = 0

image_mod = .55
x_res = 1280
y_res = 720
font_size = 38
initial_size = 55
initial_x = 350

warningStack = list()
timeBetweenWarnings = 15
lastWarnTime = {}

warnings = {}
objectWidths = {}
warnDistance = {}

allSubprocesses = {}

long_path = "/home/" + getpass.getuser() + "/CycOwl/detection/"
print(long_path)

shelf_path = long_path[:-10] + "shelf/shelf"

mp3_path = long_path + "allMP3s/"

print("Generating warnings...")
os.system("python " + long_path + "generateWarnings.py")
print("Done!")

with open(long_path + "allLabelData.txt") as allWidthsDistances:
	data = allWidthsDistances.readlines()
	for entry in data:
		currentSplit = entry.split(';')
		warnings[currentSplit[0]] = currentSplit[1]
		objectWidths[currentSplit[0]] = float(currentSplit[2])
		warnDistance[currentSplit[0]] = float(currentSplit[3].strip())

print(objectWidths)

for key in objectWidths:
	lastWarnTime[key] = time.time()
print(lastWarnTime)

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
BASE_WIDTH = 8.0
image = cv2.imread(long_path + "2ft_d_8in_w.jpg")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / BASE_WIDTH

print(focalLength)

net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson_utils.gstCamera(x_res, y_res, "0")
display = jetson_utils.glDisplay(width=704, height=396)

# Setup for text on screen
start_time = time.time()
record_start_time = True
font = jetson_utils.cudaFont(size=font_size)
initial_font = jetson_utils.cudaFont(size=initial_size)
initialText = "Ride has not begun"
warningText = ""

full_allow_path = long_path + "process.txt"
os.system("echo false > " + full_allow_path)
first_time = True
control = False
while display.IsOpen() and not control:
	shelf = shelve.open(shelf_path)
	processing = shelf["processing"]
	isTalking = shelf["talking"]
	control = shelf["stop"]
	shelf.close()
	print(processing, isTalking, control)

	currentTime = (time.time() - program_start) / 3600
	os.system("echo " + str(currentTime) + " > " + long_path + "batteryTest.txt")
	os.system("echo " + str(frames_processed) + " >> " + long_path + "batteryTest.txt")	

	if first_time:
		img, width, height = camera.CaptureRGBA()
		detections = net.Detect(img, width, height)
		display.RenderOnce(img, x=0, y=0)
		first_time = False
		# Update shelf so UI knows vision is running
		shelf = shelve.open(shelf_path)
		shelf["vision_down"] = False
		shelf.close()

	if not processing:
		warningStack.clear()
		img, width, height = camera.CaptureRGBA()
		initial_font.OverlayText(img, width, height, initialText, initial_x, 330, font.Black, font.White)

		imgOutput = jetson_utils.cudaAllocMapped(width=img.width * image_mod, 
                                         height=img.height * image_mod, 
                                         format=img.format)

		jetson_utils.cudaResize(img, imgOutput)
		display.RenderOnce(imgOutput, x=0, y=0)
		display.SetTitle("Detection not started")
		print("Not yet processing")
		record_start_time = True
		time.sleep(1.5)
	else:
		frames_processed += 1
		if record_start_time:
			warningText = "No hazards detected yet."
			start_time = time.time()
			record_start_time = False

		img, width, height = camera.CaptureRGBA()

		detections = net.Detect(img, width, height) #,overlay="none")
		overlay_time = round(time.time() - start_time)
		seconds = overlay_time % 60
		minutes = int(overlay_time / 60)
		hours = int(overlay_time / 3600)
		time_string = str(hours) + ":" + str(minutes) + ":" + str(seconds)
		print(time_string)
		font.OverlayText(img, width, height, time_string, 5, 5, font.Black, font.White)
		font.OverlayText(img, width, height, warningText, 5, 675, font.Black, font.White)

		newWidth = img.width * image_mod
		newHeight = img.height * image_mod
		imgOutput = jetson_utils.cudaAllocMapped(width=newWidth, 
                                         height=newHeight, 
                                         format=img.format)

		jetson_utils.cudaResize(img, imgOutput)

		display.RenderOnce(imgOutput, x=0, y=0)
		display.SetTitle("Object Detection | Network: {:0f} FPS".format(net.GetNetworkFPS()))

		# If there are no objects detected in the current frame
		if len(detections) == 0:
			# Pull any warnings off of the warning stack
			if len(warningStack) > 0 and not isTalking:
				allSubprocesses[warningStack[0]] = subprocess.Popen(["python3.6", long_path + "speakWarning.py", warningStack[0]])
				os.system("echo true > " + long_path + "currentlySpeaking.txt")
				warningText = "Last warning: \"" + warnings[warningStack[0]][1:] + "\" at " + time_string
				warningStack.remove(warningStack[0])

		for detection in detections:
			currentLabel = net.GetClassDesc(detection.ClassID)
			inches = -1
			closeEnough = False
			enoughTime = False
			if currentLabel in objectWidths:
				inches = distance_to_camera(BASE_WIDTH, focalLength, (BASE_WIDTH / objectWidths[currentLabel]) * detection.Width)
				if inches < warnDistance[currentLabel] * 12:
					closeEnough = True

				if abs(time.time() - lastWarnTime[currentLabel]) > timeBetweenWarnings:
					enoughTime = True
					lastWarnTime[currentLabel] = time.time()

			name = os.path.join(mp3_path, currentLabel + ".mp3")
			# print(name)
			if len(warningStack) > 0 and not isTalking:
				allSubprocesses[warningStack[0]] = subprocess.Popen(["python3.6", long_path + "speakWarning.py", warningStack[0]])
				os.system("echo true > " + long_path + "currentlySpeaking.txt")
				warningText = "Last warning: \"" + warnings[warningStack[0]][1:] + "\" at " + time_string
				warningStack.remove(warningStack[0])
				isTalking = True
			elif os.path.isfile(name) and closeEnough and enoughTime and not isTalking:
				allSubprocesses[currentLabel] = subprocess.Popen(["python3.6", long_path + "speakWarning.py", currentLabel])
				os.system("echo true > " + long_path + "currentlySpeaking.txt")
				warningText = "Last warning: \"" + warnings[currentLabel][1:] + "\" at " + time_string

			if os.path.isfile(name) and closeEnough and enoughTime and isTalking and currentLabel not in warningStack:
				warningStack.append(currentLabel)

#os.system("echo false > " + long_path + "currentlySpeaking.txt")
#os.system("echo false > " + full_allow_path)
shelf = shelve.open(shelf_path)
shelf["vision_down"] = True
shelf.close()