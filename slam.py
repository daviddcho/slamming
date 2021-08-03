#!/usr/bin/env python3
import sys
import cv2
import numpy as np
from display import Display3D
from frame import Frame
import time

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("./slam <video.mp4>")
    exit()

  disp3d = Display3D()
  cap = cv2.VideoCapture(sys.argv[1])

  CNT = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

  i = 0
  while cap.isOpened():
    ret, frame = cap.read()
    print("*** frames %d/%d ***" % (i, CNT))
    if ret == True:
      frame = cv2.resize(frame, (W, H))
      # something like process frame?
      # get key points or smt 
      # then paint
    else:
      break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pts = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
    pts = np.int0(pts)
    for f in pts:
      #print(f[0][0], f[0][1])
      x,y = f.ravel()
      cv2.circle(frame, (x,y), 3, 255, -1)

    time.sleep(.01)    
    disp3d.paint(frame)
    i += 1   


