from __future__ import division
import time
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import cv2.cv2 as cv2
from util import *
import argparse
import os
import os.path as osp
from darknet import Darknet
import pickle as pkl
import pandas as pd
import random
from gtts import gTTS
import pyttsx3
import multiprocessing
import detector

speak = True
time_between_announcements = 15


def arg_parse():
    """
    Parse arguements to the detect module

    """

    parser = argparse.ArgumentParser(description='YOLO v3 Detection Module')
    parser.add_argument("--bs", dest="bs", help="Batch size", default=1)
    parser.add_argument("--confidence", dest="confidence", help="Object Confidence to filter predictions", default=0.5)
    parser.add_argument("--nms_thresh", dest="nms_thresh", help="NMS Threshhold", default=0.4)
    parser.add_argument("--cfg", dest='cfgfile', help="Config file", default="cfg/yolov3.cfg", type=str)
    parser.add_argument("--weights", dest='weightsfile', help="weightsfile", default="yolov3.weights", type=str)
    parser.add_argument("--reso", dest='reso', help=
                        "Input resolution of the network. Increase to increase accuracy. Decrease to increase speed",
                        default="416", type=str)
    parser.add_argument("--video", dest="videofile", help="Video file to run detection on", default="video.avi",
                        type=str)

    return parser.parse_args()


args = arg_parse()
batch_size = int(args.bs)
confidence = float(args.confidence)
nms_thresh = float(args.nms_thresh)
start = 0
CUDA = torch.cuda.is_available()

num_classes = 80
classes = detector.load_classes("data/coco.names")

# Set up the neural network
print("Loading network.....")
model = Darknet(args.cfgfile)
model.load_weights(args.weightsfile)
print("Network successfully loaded")

model.net_info["height"] = args.reso
inp_dim = int(model.net_info["height"])
assert inp_dim % 32 == 0
assert inp_dim > 32

# If there's a GPU availible, put the model on GPU
if CUDA:
    model.cuda()

# Set the model in evaluation mode
model.eval()

color_labels = {"Name": "color_labels"}
time_labels = {}


def write(x, results):
    # c1 = tuple(x[1:3].int())
    # c2 = tuple(x[3:5].int())
    c1, c2 = (int(x[1]), int(x[2])), (int(x[3]), int(x[4]))
    img = results
    cls = int(x[-1])
    label = "{0}".format(classes[cls])
    if label in color_labels.keys():
        color = color_labels[label]
    else:
        color = random.choice(colors)
        color_labels[label] = color
    # speech = multiprocessing.Process(target=text_to_speech(label, time_labels))
    # speech.start()
    # speech.join()
    if speak:
        text_to_speech(label, time_labels)
    # cv2.rectangle(img, c1, c2, color, 1)
    cv2.rectangle(img, c1, (int(np.float32(c2[0])), int(np.float32(c2[1]))), color, 1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    t_size = cv2.getTextSize(label, font, 1, 1)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
    # cv2.rectangle(img, c1, c2, color, -1)
    cv2.rectangle(img, c1, (int(np.float32(c2[0])), int(np.float32(c2[1]))), color, -1)
    # cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225, 255, 255], 1)
    cv2.putText(img, label, (c1[0], int(np.float32(c1[1] + t_size[1] + 4))), font, 1, [255, 255, 255], 1)
    return img


def text_to_speech(label, dic):
    # if not osp.exists('mp3s'):
    #     os.mkdir('mp3s')
    #
    # mp3_file = 'mp3s/' + label + '.mp3'
    engine = pyttsx3.init()
    if label not in dic.keys():
        # if not osp.exists(mp3_file):
        #     audio = gTTS(text=label, lang="en", slow=False)
        #     audio.save(mp3_file)
        # os.system("start " + mp3_file)
        dic[label] = time.time()
        engine.say(label)
        engine.runAndWait()
    else:
        if abs(time.time() - dic[label]) > time_between_announcements:
            # os.system("start " + mp3_file)
            dic[label] = time.time()
            engine.say(label)
            engine.runAndWait()



# Detection phase

# videofile = args.videofile  # or path to the video file.
#
# cap = cv2.VideoCapture(videofile)

cap = cv2.VideoCapture(1)  # 0 for webcam, 1 for usb cam

if not cap.isOpened():
    cap = cv2.VideoCapture(0)

assert cap.isOpened(), 'Cannot capture source'

frames = 0
start = time.time()

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        img = detector.prep_image(frame, inp_dim)
        #        cv2.imshow("a", frame)
        im_dim = frame.shape[1], frame.shape[0]
        im_dim = torch.FloatTensor(im_dim).repeat(1, 2)

        if CUDA:
            im_dim = im_dim.cuda()
            img = img.cuda()

        with torch.no_grad():
            output = model(Variable(img, volatile=True), CUDA)
        output = write_results(output, confidence, num_classes, nms_conf=nms_thresh)

        if type(output) == int:
            frames += 1
            print("FPS of the video is {:5.4f}".format(frames / (time.time() - start)))
            cv2.imshow("frame", frame)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            continue

        im_dim = im_dim.repeat(output.size(0), 1)
        scaling_factor = torch.min(416 / im_dim, 1)[0].view(-1, 1)

        output[:, [1, 3]] -= (inp_dim - scaling_factor * im_dim[:, 0].view(-1, 1)) / 2
        output[:, [2, 4]] -= (inp_dim - scaling_factor * im_dim[:, 1].view(-1, 1)) / 2

        output[:, 1:5] /= scaling_factor

        for i in range(output.shape[0]):
            output[i, [1, 3]] = torch.clamp(output[i, [1, 3]], 0.0, im_dim[i, 0])
            output[i, [2, 4]] = torch.clamp(output[i, [2, 4]], 0.0, im_dim[i, 1])

        classes = detector.load_classes('data/coco.names')
        colors = pkl.load(open("pallete", "rb"))

        list(map(lambda x: write(x, frame), output))

        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        frames += 1
        print(time.time() - start)
        print("FPS of the video is {:5.2f}".format(frames / (time.time() - start)))
    else:
        break
