import numpy as np
import cv2

def extract_features(img):
  """
  """
  orb = cv2.ORB_create()
  # detection
  #img = cv2.cvtColor(np.float32(img), cv2.COLOR_BGR2GRAY)
  pts = cv2.goodFeaturesToTrack(np.mean(img, axis=2).astype(np.uint8), 3000, qualityLevel=0.01, minDistance=10)
  #pts = np.int0(pts)

  # extraction
  kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in pts]
  kps, des = orb.compute(img, kps)

  # return pts and descriptors
  kps = np.array([(kp.pt[0], kp.pt[1]) for kp in kps]).astype(np.uint8)
  return kps, des

def match_frames(f1, f2):
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
  matches = bf.match(f1.des, f2.des) 


class Frame(object):
  def __init__(self, img):
    self.img = img
    self.kps, self.des = extract_features(self.img) 

  def annotate(self):
    for kp in self.kps:
      x,y = kp
      cv2.circle(self.img, (x,y), 3, (0,255,0), -1)
    return self.img

  

