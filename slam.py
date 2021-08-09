#!/usr/bin/env python3
import sys
import cv2
import numpy as np
from display import Display3D
from frame import Frame, denormalize, match_frames, extract_features
import time

frames = []
def process_frame(img, K):
  frame = Frame(img, K)
  frames.append(frame)
  if len(frames) <= 1:
    return 

  ret = match_frames(frames[-1], frames[-2])
  for pt1, pt2 in ret:
    u1, v1 = denormalize(K, pt1)
    u2, v2 = denormalize(K, pt2)
    cv2.circle(img, (u1, v1), color=(0,255,0), radius=3)
    cv2.line(img, (u1, v1), (u2, v2), color=(255,0,0))
  
  return np.array(img)

def display(img):
  if img is not None:
    cv2.imshow("img", img)
    cv2.waitKey(1)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("./slam <video.mp4>")
    exit()

  cap = cv2.VideoCapture(sys.argv[1])

  CNT = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  if W > 1000: 
    W = W//2
    H = H//2

  #disp3d = Display3D(W, H)
  # camera instrinics
  F = 270 
  K = np.array([[F, 0, W//2],
               [0, F, H//2],
               [0, 0,    1]])

  i = 0
  while cap.isOpened():
    ret, frame = cap.read()
    print("*** frames %d/%d ***" % (i, CNT))
    if ret == True:
      frame = cv2.resize(frame, (W, H))
      img = process_frame(frame, K)
    else:
      break
    #time.sleep(1)    
    
    display(img)
    #disp3d.paint(img)
    i += 1   


