from multiprocessing import Process, Queue
import numpy as np
import OpenGL.GL as gl 
import pypangolin as pangolin
import cv2

class Display3D(object): 
  def __init__(self, wi, hi):
    #self.wi, self.hi = wi, hi
    self.state = None
    self.q = Queue()
    self.vp = Process(target=self.viewer_thread, args=(self.q,))
    self.vp.daemon = True
    self.vp.start() 

  def viewer_thread(self, q):
    w, h = 1024, 768 
    self.viewer_init(w, h)
    while 1:
      self.viewer_refresh(q)

  def viewer_init(self, w, h):
    pangolin.CreateWindowAndBind("Main", w, h) 
    gl.glEnable(gl.GL_DEPTH_TEST)
    
    # Define Projection and initial ModelView matrix
    self.scam = pangolin.OpenGlRenderState(
      pangolin.ProjectionMatrix(w, h, 420, 420, w//2, h//2, 0.2, 100),
      pangolin.ModelViewLookAt(-2, 2, -2, 0, 0, 0, pangolin.AxisDirection.AxisY))
    self.handler = pangolin.Handler3D(self.scam)
    
    # Create Interactive View in window
    self.dcam = pangolin.CreateDisplay()
    self.dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -w/h)
    self.dcam.SetHandler(self.handler)

    """
    self.dimg = pangolin.Display("image")
    self.dimg.SetBounds(0.0, self.hi/h, self.wi/w, 1.0, w/h)
    self.dimg.SetLock(pangolin.Lock.LockLeft, pangolin.Lock.LockTop)
    self.texture = pangolin.GlTexture(self.wi, self.hi, gl.GL_RGB, False, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)
    self.img = np.ones((self.hi, self.wi, 3), dtype="uint8")*255
    """

  def viewer_refresh(self, q): 
    while not self.q.empty():
      self.state = self.q.get()

    if self.state is not None:
      self.img = self.state
      self.img = self.img[::-1, :]
      self.img = cv2.resize(self.img, (self.wi, self.hi))

    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    self.dcam.Activate(self.scam)

    """
    self.texture.Upload(self.img, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)
    self.dimg.Activate()
    gl.glColor3f(1.0, 1.0, 1.0)
    self.texture.RenderToViewport()
    """

    pangolin.FinishFrame()

  def paint(self, img): 
    if self.q is None:
      return

    self.q.put(np.array(img))

