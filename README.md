# TorontoSkatepark_TD_PVL
Toronto Skateboard Committee Projection mapping Tool - for planning skate parks

**Step Zero:**
Touchdesigner grabs the video capture from the Kinect.
Post-processing filters can be applied to sharpen/ Monochrome to adjust image quality

_If the camera is not calibrated
**Step One “GetCameraMatrix”**
Take photos of checkerboard needs a large amount spanning the entire frame and layered
A camera matrix is constructed for the OpenCV_Aruco.py to use 
Save it as a “.npz” file

**Step Two “SendSocket”**
Sends Post-processing adjusted video to OpenCV_Aruco.py as convert numpy array/ over socket

**Step Three “OpenCv_Aruco”**
Uses numpy image to estimate pose using “.npz” camera matrix created in “GetCameraMartix.tox”
sends the tx ty tz rx ry rz data over to Touchdesigner over OSC

**Step Four:**
Touchdesigner projects the data as instanced objects in a space

**Step Five: “KinectCalibration”**
The projector and Kinect need to be calibrated. Since “OpenCv_Aruco” is using the same color image as the reprojected point cloud all the Aruco calculated points should be in relatively (needs some adjusting Work in progress) the same position. Calibration will allow the projector to project the instanced 3D object over the marker


![Test Image 2](/ProcessImage(2).png)


**Step Five:**
Final adjustments on the 3D Camera for accurate projection
