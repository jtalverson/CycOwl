import argparse
import time
import os
import getpass

parser = argparse.ArgumentParser()
parser.add_argument('label', type=str)
args = parser.parse_args()

long_path = "/home/" + getpass.getuser() + "/CycOwl/detection/"
mp3_path = long_path + "allMP3s/"

print("Subprocess received label of: " + args.label)
os.system("mpg321 -o alsa \"" + mp3_path + args.label + ".mp3\"")
os.system("echo false > " + long_path + "currentlySpeaking.txt")
