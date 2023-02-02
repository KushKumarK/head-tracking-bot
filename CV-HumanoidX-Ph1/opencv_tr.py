import cv2
import threading
import serial
import cvzone
import numpy as np
import time
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector

try:
        ser = serial.Serial(baudrate='9600',port='COM12')
except:
        print("Error")
 
cap = cv2.VideoCapture(1)
detect = HandDetector(detectionCon=0.8, maxHands=1)
detector = FaceDetector()
center = [0,0]
a=0
dist =0
def cvCode():
        global center,a,dist
        while True:
                success,img=cap.read()
                h,w,c= img.shape
                previousX=h//2
                #ch = int(input("Enter 0 for Face tracking and 1 for Hands: "))
                time.sleep(0.005)
##                if (ch ==0):
##                        img, faces = detector.findFaces(img)
##                        if faces:
##                                center = list(faces[0]["center"])
##                                dist = previousX-float(center[0])
##                                center[0] = dist
##                        else:
##                                dist = 0
##                                center[0] = dist
##                        
##                else:
                hands,img=detect.findHands(img)
                if hands:
                        hand1 = hands[0]
                        center = list(hand1['center'])
                        dist = previousX-float(center[0])
                        center[0] = dist
                        #ser.write(msg.encode())
                        #time.sleep(1)
                        #print(center[1])
                else:
                        dist = 0
                        center[0] = dist
                cv2.imshow("Image",img)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        a = 1
                        break

def sendCode():
        while True:
                global center,a
                msg = str(center[0])            
                ser.write(msg.encode())
                time.sleep(1)
                #print(center[0])
                if a==1:
                        break

t1 =  threading.Thread(target = cvCode)
t2 =  threading.Thread(target = sendCode)

t1.start()
t2.start()

t1.join()
t2.join()

ser.close()
cap.release()
cv2.destroyAllWindows()

