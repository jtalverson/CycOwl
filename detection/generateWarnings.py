from gtts import gTTS
import getpass
import os

language = 'en'

speak = False

long_path = "/home/" + getpass.getuser() + "/CycOwl/detection/"

allMP3s = long_path + "allMP3s/"

if not os.path.isdir(allMP3s):
	os.system("mkdir " + allMP3s)

speechWarnings = {}

with open(long_path + "allLabelData.txt") as allWarnings:
	warnings = allWarnings.readlines()
	for warning in warnings:
		currentSplit = warning.split(';')
		speechWarnings[currentSplit[0]] = currentSplit[1]

# print (speechWarnings)
for speech in speechWarnings:
	current = gTTS(text=speechWarnings[speech], lang=language, slow=False)
	current.save(allMP3s + speech + ".mp3")

if speak:
	for filename in os.listdir(allMP3s):
		name = os.path.join(allMP3s, filename)
		if os.path.isfile(name):
			print (name)
			os.system("mpg321 \"" + name + "\"")
