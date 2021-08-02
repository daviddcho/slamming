#!/usr/bin/env python3
import sys
import cv2
from display import Display3D
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

    time.sleep(.01)    
    disp3d.paint(frame)
    i += 1   


