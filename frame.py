import numpy as np
np.set_printoptions(suppress=True)
import cv2

from skimage.measure import ransac
from skimage.transform import FundamentalMatrixTransform, EssentialMatrixTransform

def poseRt(R, t):
  ret = np.eye(4)
  ret[:3, :3] = R
  ret[:3, 3] = t 
  return ret

def extractRt(E):
  # https://stackoverflow.com/questions/20614062/pose-from-fundamental-matrix-and-vice-versa
  W = np.mat([[0,-1,0],[1,0,0],[0,0,1]], dtype=float)
  U,d,Vt = np.linalg.svd(E)
  assert np.linalg.det(U) > 0
  if np.linalg.det(Vt) < 0:
    Vt *= -1.0
  R = np.dot(np.dot(U, W), Vt)
  if np.sum(R.diagonal()) < 0: 
    R = np.dot(np.dot(U,W.T), Vt)
  t = U[:, 2]
  #Rt = np.concatenate((R, t.reshape(3,1)), axis=1)
  return poseRt(R, t)
 
def extract_features(img):
  orb = cv2.ORB_create()
  # detection
  gimg = cv2.cvtColor(np.float32(img), cv2.COLOR_BGR2GRAY)
  pts = cv2.goodFeaturesToTrack(gimg, 3000, qualityLevel=0.01, minDistance=7)

  # extraction
  kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in pts]
  kps, des = orb.compute(img, kps)

  # return pts and descriptors
  kps = np.array([(int(kp.pt[0]), int(kp.pt[1])) for kp in kps])
  return kps, des

def match_frames(f1, f2):
  bf = cv2.BFMatcher(cv2.NORM_HAMMING)#, crossCheck=True)
  matches = bf.knnMatch(f1.des, f2.des, k=2) 

  # Lowe's ratio test
  ret = []
  for m, n in matches:
    if m.distance < 0.75*n.distance: 
      p1 = f1.pts[m.queryIdx]
      p2 = f2.pts[m.trainIdx]
      ret.append((p1, p2))

  assert len(ret) >= 8
  ret = np.array(ret)
  
  # fit matrix
  model, inliers = ransac((ret[:, 0], ret[:, 1]), 
                          EssentialMatrixTransform,
                          #FundamentalMatrixTransform,
                          min_samples=8,
                          #residual_threshold=1,
                          residual_threshold=.005,
                          max_trials=100)

  ret = ret[inliers]
  Rt = extractRt(model.params) 

  return ret, Rt
  
# turn [[x,y]] -> [[x,y,1]] (into homogeneous coords)
def add_ones(x):
  return np.concatenate([x, np.ones((x.shape[0], 1))], axis=1)

# normalize coords
def normalize(Kinv, pts):
  ret = add_ones(pts).T
  ret = np.dot(Kinv, ret).T[:, 0:2]
  return ret

# going back to u,v coords
def denormalize(K, pt):
  ret = np.dot(K, np.array([pt[0], pt[1], 1.0]))
  #ret /= ret[2]
  return int(round(ret[0])), int(round(ret[1]))

class Frame(object):
  def __init__(self, img, K):
    self.img = img
    self.K = K
    self.Kinv = np.linalg.inv(self.K)
    self.pose = np.eye(4)

    pts, self.des = extract_features(self.img) 
    self.pts = normalize(self.Kinv, pts)

