# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
cap = PiCamera()
cap.resolution = (640, 480)
cap.framerate = 32
rawCapture = PiRGBArray(cap, size=(640, 480))
time.sleep(0.1)

faceCascade = cv2.CascadeClassifier("lbpcascade_frontalface_improved.xml")

# allow the camera to warmup

# capture frames from the camera
for frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.face.drawFacemarks(frame,np.array([(x,y),(x+w,y),(x+w,y+h),(x,y+h)]),(255,255,255))

    cv2.imshow('frame', gray)
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.close()
