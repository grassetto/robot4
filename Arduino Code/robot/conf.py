#FILE DA TERMINARE *********************************************


import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2

#********CONFIG********
conf = open("conf/conf.txt", "r")
#**********************
# eval restituisce il valore numerico del del file
#Creo l'oggetto videocamera
video = PiCamera()
video.resolution = (640,480)
#Creo numpy array dell'immagine RGB 
rawValue = PiRGBArray(video, size=(640,480))

for frame in video.capture_continuous(rawValue, format="bgr", use_video_port='true'):
    
    nero = eval(conf.readLines[4][7:])
    #Creo l'immagine
    img = frame.array
    #Creo una regione d'interesse dell'immagine
    roi = img[200:300, 0:]
    #Trovo la linea
    linea = cv2.inRange(roi, (0,0,0), (nero, nero, nero))
    #Definisco la grandezza del kernel
    pxApprox = np.ones((3,3), np.uint8)
    #Approssimo la lettura della linea 
    linea = cv2.erode(linea, pxApprox, iterations=10)
    linea = cv2.dilate(linea, pxApprox, iterations=10)
    #Definisco il bordo
    laplace = cv2.Laplacian(linea, cv2.CV_8UC1)
    im, cont, hier = cv2.findContours(linea, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #Controll che ci sia la linea
    if len(cont) > 0:
        for i in range(0,len(cont)):
            #Creo un rettangolo che contorna la linea        
            x,y,w,h = cv2.boundingRect(cont[i])
            cv2.rect(img, (x+int(w/2),200),(x+int(w/2),300),(255,255,0),2)                                    
    cv2.imshow("Robot4", img)
    rawValue.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()
video.close()
