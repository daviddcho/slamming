#!/usr/bin/env python3
import numpy as np
import OpenGL.GL as gl
import pypangolin as pangolin

w, h = 640, 640

pangolin.CreateWindowAndBind("Main", w, h) 
gl.glEnable(gl.GL_DEPTH_TEST)

# Define Projection and intial ModelView matrix
scam = pangolin.OpenGlRenderState(
  pangolin.ProjectionMatrix(w, h, 420, 420, w//2, h//2, 0.2, 100),
  pangolin.ModelViewLookAt(-2, 2, -2, 0, 0, 0, pangolin.AxisDirection.AxisY))
handler = pangolin.Handler3D(scam)

# Create Interactive View in window
dcam = pangolin.CreateDisplay()
dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -w/h)
dcam.SetHandler(handler)

while not pangolin.ShouldQuit():
  gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
  gl.glClearColor(1.0, 1.0, 1.0, 1.0)
  dcam.Activate(scam)

  # Render OpenGL Cube
  pangolin.glDrawColouredCube()

  # Draw Point Cloud
  points = np.random.random((100000, 3)) * 10
  colors = np.zeros((len(points), 3))
  colors[:,1] = 1 - points[:,0] / 10.
  colors[:,2] = 1 - points[:,1] / 10.
  colors[:,0] = 1 - points[:,2] / 10.

  gl.glPointSize(3)
  gl.glColor3f(1.0, 0.0, 0.0)
  pangolin.DrawPoints(points, colors)

  pangolin.FinishFrame()

 
