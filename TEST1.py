# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np;
import pyautogui
width,height=pyautogui.size()





params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 20
params.maxThreshold = 150


# Filter by Area.
params.filterByArea = True
params.minArea = 30
params.maxArea = 100

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.01

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.5
    
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01





 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)

X1=160
X2=400
Y1=160
Y2=450
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
     image = frame.array
     crop_img = image[X1:X2, Y1:Y2]
     cv2.imshow("cropped", crop_img)
     cv2.imwrite("TEMP.jpg",crop_img)
     im = cv2.imread("TEMP.jpg", cv2.IMREAD_GRAYSCALE)
     key = cv2.waitKey(1) & 0xFF
     ver = (cv2.__version__).split('.')
     if int(ver[0]) < 3 :
               detector = cv2.SimpleBlobDetector(params)
     else : 
               detector = cv2.SimpleBlobDetector_create(params)

     keypoints = detector.detect(im)
     if len(keypoints)>0:
          x = keypoints[0].pt[0] 
          y = keypoints[0].pt[1]
          x1=width-(((x)/(X2-X1))*width)
          y1=((y)/(Y2-Y1))*height
          if((x1<=previous_x1+50) & (x1>=previous_x1-50) &(y1<=previous_y1+50) &(y1>=previous_y1-50)):
               break
          else:
               pyautogui.moveTo(x1,y1)
               pyautogui.click()
               previous_x1=x1;
               previous_y1=y1;
               print (x1)
               print (y1)
     else:
          x1=0;
          y1=0;
          
          
     im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)



     cv2.imwrite("DETECT.jpg", im_with_keypoints)

     cv2.imshow("Keypoints", im_with_keypoints)
      
     # clear the stream in preparation for the next frame
     rawCapture.truncate(0)
      
     # if the `q` key was pressed, break from the loop
     if key == ord("q"):
          break
