import argparse
import time
import os
import getpass
import shelve

parser = argparse.ArgumentParser()
parser.add_argument('label', type=str)
args = parser.parse_args()

long_path = "/home/" + getpass.getuser() + "/CycOwl/detection/"
mp3_path = long_path + "allMP3s/"

shelf_path = long_path[:-10] + "shelf/shelf"
print(shelf_path)
shelf = shelve.open(shelf_path)
shelf["talking"] = True
shelf.close()
#time.sleep(10000)

print("Subprocess received label of: " + args.label)
#os.system("mpg321 -o alsa \"" + mp3_path + args.label + ".mp3\"")
os.system("mpg321 \"" + mp3_path + args.label + ".mp3\"")
#os.system("echo false > " + long_path + "currentlySpeaking.txt")

shelf = shelve.open(shelf_path)
shelf["talking"] = False
shelf.close()
