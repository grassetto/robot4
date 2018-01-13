#IMPORT NECESSARI


import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2

#********DEBUG********
debug = True
#*********************
#Variabili
nero = 50
#Creo l'oggetto videocamera
video = PiCamera()
video.resolution = (640,480)
#Creo numpy array dell'immagine RGB 

rawValue = PiRGBArray(video, size=(640,480))
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
#********DEBUG********
if(debug):
    viddebug = cv2.VideoWriter('debug.avi',fourcc, 20.0, (640, 480))
#*********************
for frame in video.capture_continuous(rawValue, format="bgr", use_video_port='true'):
    img = frame.array
    linea = cv2.inRange(img, (0,0,0), (nero, nero, nero))
    #********DEBUG********
    if(debug):
        viddebug.write(img)
    #*********************                                      
    cv2.imshow("Robot4", linea)

    rawValue.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
#********DEBUG********
if(debug):
    viddebug.release()
#*********************
cv2.destroyAllWindows()
video.close()