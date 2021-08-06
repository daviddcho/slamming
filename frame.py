import numpy as np
import cv2

def extract_features(img):
  orb = cv2.ORB_create()
  # detection
  #img = cv2.cvtColor(np.float32(img), cv2.COLOR_BGR2GRAY)
  pts = cv2.goodFeaturesToTrack(np.mean(img, axis=2).astype(np.uint8), 3000, qualityLevel=0.01, minDistance=7)
  #pts = np.int0(pts)

  # extraction
  kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in pts]
  kps, des = orb.compute(img, kps)

  # return pts and descriptors
  kps = np.array([(kp.pt[0], kp.pt[1]) for kp in kps]).astype(np.uint8)
  return kps, des

def match_frames(f1, f2):
  bf = cv2.BFMatcher(cv2.NORM_HAMMING)#, crossCheck=True)
  matches = bf.knnMatch(f1.des, f2.des, k=2) 

  # Lowe's ratio test
  ret = []
  for m, n in matches:
    if m.distance < 0.75*n.distance: 
      p1 = f1.pts[m.queryIdx]
      p2= f2.pts[m.trainIdx]
      ret.append((p1, p2))
  #assert len(ret) >= 8
  ret = np.array(ret)

  return ret
  
# turn [[x,y]] -> [[x,y,1]]
def add_ones(x):
  return np.concatenate([x, np.ones((x.shape[0], 1))], axis=1)

def normalize(Kinv, pts):
  return np.dot(Kinv, add_ones(pts).T).T[:, 0:2]

def denormalize(K, pt):
  ret = np.dot(K, np.array([pt[0], pt[1], 1.0]))
  ret /= ret[2]
  return int(round(ret[0])), int(round(ret[1]))

class Frame(object):
  def __init__(self, img, K):
    self.img = img
    self.K = K
    self.Kinv = np.linalg.inv(self.K)

    pts, self.des = extract_features(self.img) 
    self.pts = normalize(self.Kinv, pts)

  def annotate(self):
    for pt in self.pts:
      x, y = denormalize(self.K, pt)
      cv2.circle(self.img, (x,y), 3, (0,255,0), -1)
    return self.img


