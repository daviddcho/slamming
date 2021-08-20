working towards visual-inertial SLAM (using camera and IMU)

currently spotty localization (it starts drifting) and not good 3d map (cv2 triangulate is bad i think)

![demo](/demo.png)

Pipeline:
1. Detect features (shi-tomasi)
2. Compute descriptors (orb)
3. Match features (lowes ratio test)
4. Filter matched features (ransac)
  * you can find focal from fundamental matrix for camera calibration
5. Extract (pose) Rt from essential matrix
6. Triangulate the points into homogenuous 3d coords (direct linear triangulation)

EKF looks complicated:
* EKF for imu and vision: https://sci-hub.se/10.1109/ROBOT.2007.364024
  * implementation: https://github.com/uoip/stereo_msckf
* https://github.com/AtsushiSakai/PythonRobotics/tree/master/Localization/extended_kalman_filter

resources:
* ORB-SLAM: https://arxiv.org/pdf/1502.00956.pdf
* https://github.com/luigifreda/pyslam
* LSD-SLAM, MonoSLAM
* a survey: https://fzheng.me/2016/03/13/slam-papers/#visual-inertial-slam

computer vision basics: https://cseweb.ucsd.edu/classes/sp04/cse252b
