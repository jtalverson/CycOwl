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

warningStack = list()
timeBetweenWarnings = 15
lastWarnTime = {}

warnings = {}
objectWidths = {}
warnDistance = {}

allSubprocesses = {}

long_path = "/home/" + getpass.getuser() + "/CycOwl/detection/"
print(long_path)

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
camera = jetson_utils.gstCamera(1280, 720, "0")
display = jetson_utils.videoOutput("display://0")

os.system("pacmd set-default-sink alsa_output.usb-Solid_State_System_Co._Ltd._USB_PnP_Audio_Device_000000000000-00.analog-stereo")

# Setup for text on screen
start_time = time.time()
record_start_time = True
font = jetson_utils.cudaFont(size=26)
warningText = ""

full_allow_path = long_path + "process.txt"
os.system("echo false > " + full_allow_path)
first_time = True
while True:
	if first_time:
		img, width, height = camera.CaptureRGBA()
		detections = net.Detect(img, width, height)
		display.Render(img)
		first_time = False

	if not display.IsStreaming():
		break

	startProcessing = False
	with open(full_allow_path) as allow:
		allowance = allow.readlines()
		for line in allowance:
			if line.strip() == "true":
				startProcessing = True

	if not startProcessing:
		img, width, height = camera.CaptureRGBA()
		display.Render(img)
		display.SetStatus("Detection not started")
		print("Not yet processing")
		record_start_time = True
		time.sleep(1.5)
	else:
		if record_start_time:
			warningText = "No hazards detected yet."
			start_time = time.time()
			record_start_time = False

		img, width, height = camera.CaptureRGBA()
		detections = net.Detect(img, width, height) #,overlay="none")
		font.OverlayText(img, width, height, str(round(time.time() - start_time, 2)), 5, 5)
		font.OverlayText(img, width, height, warningText, 5, 675)
		display.Render(img)
		display.SetStatus("Object Detection | Network: {:0f} FPS".format(net.GetNetworkFPS()))

		# If there are no objects detected in the current frame
		if len(detections) == 0:
			# Update the is talking variable
			isTalking = False
			with open(long_path + "currentlySpeaking.txt") as speakControl:
				for line in speakControl.readlines():
					if line.strip() == "true":
						isTalking = True
			# print(isTalking)
			# Pull any warnings off of the warning stack
			if len(warningStack) > 0 and not isTalking:
				allSubprocesses[warningStack[0]] = subprocess.Popen(["python3.6", long_path + "speakWarning.py", warningStack[0]])
				os.system("echo true > " + long_path + "currentlySpeaking.txt")
				warningText = "Last warning: \"" + warnings[warningStack[0]][1:] + "\" at " + str(round(time.time() - start_time, 2))
				warningStack.remove(warningStack[0])

		for detection in detections:
			currentLabel = net.GetClassDesc(detection.ClassID)
			inches = -1
			closeEnough = False
			enoughTime = False
			isTalking = False
			if currentLabel in objectWidths:
				inches = distance_to_camera(BASE_WIDTH, focalLength, (BASE_WIDTH / objectWidths[currentLabel]) * detection.Width)
				if inches < warnDistance[currentLabel] * 12:
					closeEnough = True

				if abs(time.time() - lastWarnTime[currentLabel]) > timeBetweenWarnings:
					enoughTime = True
					lastWarnTime[currentLabel] = time.time()

			with open(long_path + "currentlySpeaking.txt") as speakControl:
				for line in speakControl.readlines():
					if line.strip() == "true":
						isTalking = True
			# print(isTalking)

			# print ("Close %s Time %s Talking %s" % (closeEnough, enoughTime, isTalking))

			name = os.path.join(mp3_path, currentLabel + ".mp3")
			# print(name)
			if len(warningStack) > 0 and not isTalking:
				allSubprocesses[warningStack[0]] = subprocess.Popen(["python3.6", long_path + "speakWarning.py", warningStack[0]])
				os.system("echo true > " + long_path + "currentlySpeaking.txt")
				warningText = "Last warning: \"" + warnings[warningStack[0]][1:] + "\" at " + str(round(time.time() - start_time, 2))
				warningStack.remove(warningStack[0])
				isTalking = True
			elif os.path.isfile(name) and closeEnough and enoughTime and not isTalking:
				allSubprocesses[currentLabel] = subprocess.Popen(["python3.6", long_path + "speakWarning.py", currentLabel])
				os.system("echo true > " + long_path + "currentlySpeaking.txt")
				warningText = "Last warning: \"" + warnings[currentLabel][1:] + "\" at " + str(round(time.time() - start_time, 2))

			if os.path.isfile(name) and closeEnough and enoughTime and isTalking and currentLabel not in warningStack:
				warningStack.append(currentLabel)

os.system("echo false > " + long_path + "currentlySpeaking.txt")
os.system("echo false > " + full_allow_path)
