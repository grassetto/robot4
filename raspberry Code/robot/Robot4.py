#IMPORT NECESSARI
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2

#********CONFIG********
conf = open("conf/conf.txt", "r")
mvf = conf.readlines()
conf.close()
#**********************
# eval restituisce il valore numerico del del file
#********DEBUG********
debug = eval(mvf[3][7:])

#*********************
#Variabili ***********
nero = eval(mvf[4][7:])
# End Variabili ******
#Creo l'oggetto videocamera
video = PiCamera()
video.resolution = (640,480)
#Creo numpy array dell'immagine RGB 
rawValue = PiRGBArray(video, size=(640,480))
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
#********DEBUG********
if(debug):
    viddebug = cv2.VideoWriter('debug/vid/debug.avi',fourcc, 30.0, (640, 480))
#*********************
for frame in video.capture_continuous(rawValue, format="bgr", use_video_port='true'):
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
    bordo = cv2.GaussianBlur(linea, (3,3), 5)
    laplace = cv2.Laplacian(linea, cv2.CV_8UC1)
    im, cont, hier = cv2.findContours(linea, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #Controll che ci sia la linea
    if len(cont) > 0:
        for i in range(0,len(cont)):
            #Creo un rettangolo che contorna la linea        
            x,y,w,h = cv2.boundingRect(cont[i])
            #Trasformo in interi i numeri appena ricavati
            #Disegno il contorno
            #cv2.drawContours(img,[cord_rect],0,(0,255,0),2)
            cv2.line(img, (x+int(w/2),200),(x+int(w/2),300),(255,255,0),2)
            #Genero le coorinate di 2 punti
            
            #Disegno i 4 punti
            #cv2.rectangle(img,(x,y),(w+x,h+y),(33,79,91),2)
    #********DEBUG********
    if(debug):
        viddebug.write(img)
    #*********************                                      
    cv2.imshow("Robot4", img)
    rawValue.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
#********DEBUG********
if(debug):
    viddebug.release()
#*********************
cv2.destroyAllWindows()
video.close()
