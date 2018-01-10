import picamera
import picamera.array
import sys
import numpy as np
black= 100
arrayImg = []
txt=open('arrayTxt.txt', 'w+')

with picamera.PiCamera() as camera:
    camera.resolution = (100, 100)
    with picamera.array.PiRGBArray(camera) as output:
        camera.capture(output, 'rgb')
        arrayImg = output.array.copy()
    for x in range (0,100):
        for y in range (0,100):
            if arrayImg[x,y,0] < 80 and arrayImg[x,y,1] < 80 and arrayImg[x,y,2] < 80:
                arrayImg[x,y] = 1
            else:
                arrayImg[x,y] = 0

    for y in range (0,100):
        txt.write("\n")
        for x in range (0,100):
            txt.write(np.array_str(arrayImg[x,y]))
            txt.write(" ")
txt.close()
print("end")
            
            
