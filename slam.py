#!/usr/bin/env python3
import sys
import cv2
import numpy as np
from display import Display3D
from frame import Frame, denormalize, match_frames, extract_features
import time

pts = []
poses = []
frames = []
def process_frame(img, K):
  frame = Frame(img, K)
  frames.append(frame)
  if len(frames) <= 1:
    return 

  matches, Rt = match_frames(frames[-1], frames[-2])
  frames[-1].pose = np.dot(Rt, frames[-2].pose)
  print(frames[-1].pose)
  poses.append(frames[-1].pose)

  pts4d = cv2.triangulatePoints(frames[-1].pose[:3], frames[-2].pose[:3], matches[:,0].T, matches[:,1].T).T
  pts4d /= pts4d[:,3:]
  for p in pts4d:
    p *= -1.0
    pts.append(p)

  print("%d matches" % len(matches))
  for pt1, pt2 in matches:
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

  disp3d = Display3D(W, H)
  # camera instrinics
  F = 270 #190.97
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
    disp3d.paint(poses, pts)
    i += 1   


