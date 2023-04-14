from gtts import gTTS

import os

language = 'en'

allMP3s = "./allMP3s/"

if not os.path.isdir(allMP3s):
	os.system("mkdir " + allMP3s)

speechWarnings = {}

with open("./warnings.txt") as allWarnings:
	warnings = allWarnings.readlines()
	for warning in warnings:
		currentSplit = warning.split(',')
		speechWarnings[currentSplit[0]] = currentSplit[1].strip()

print (speechWarnings)
for speech in speechWarnings:
	current = gTTS(text=speechWarnings[speech], lang=language, slow=False)
	current.save(allMP3s + speech + ".mp3")

#for filename in os.listdir(allMP3s):
#	name = os.path.join(allMP3s, filename)
#	if os.path.isfile(name):
		# print (name)
		# os.system("mpg321 \"" + name + "\"")
