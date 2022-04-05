#!/usr/bin/env python
# coding: utf-8
"""
Object Detection (On Pi Camera) From TF2 Saved Model
=====================================
"""
from PIL import Image
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging (1)
# import pathlib
import tensorflow as tf
import cv2
import argparse
from threading import Thread
from WOB import WOB
from cam import cam
from detector import detector
from comms import comms
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings


comm = comms.sd


stream = cam(resolution=(640,480),framerate=30).start()
detection = detector.detect

print('Running inference for PiCamera')

while True:

    # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    frame = stream.read()
    
    image, item, count = detection(frame)
    
    if count <= 12:
      image = cv2.resize(image,(600,600))
      cv2.imshow('Object Counter', image)
      print('no board found')
      comm.putString('info', 'no board found')
    else:
      # image, max_area = getWOB(frame)
      image, max_area = WOB.getWOB(frame)
      cv2.imshow('result', cv2.resize(image,(600,600)))
      deliver, ret = WOB.sort_grid(image,item)
      image = cv2.resize(image,(600,600))
      # cv2.putText (image,'Total Detections : ' + str(count),(10,25),cv2.FONT_HERSHEY_SIMPLEX,1,(70,235,52),2,cv2.LINE_AA)
      cv2.imshow('Object Counter', image)
      print("max area:", max_area)
      comm.putString('max area:', max_area)
      comm.putStringArray('deliver', str(deliver))
      comm.putStringArray('return', str(ret))

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
print("Done")
