import threading

import serial
import time
import cv2
import mediapipe as mp
#import keyboard

ser=serial.Serial(port="COM12",baudrate=9600)
ser.timeout=1


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(1)

ishandDetected=0
val=0
dist=0


def serial():
    global val,dist,ishandDetected
    while True:
        if val==1:
            print("done")
            break
        if ishandDetected==1:
            # print("distance is: ",dist," ishanddetected: ",ishandDetected)
            ser.write((str(dist)).encode())
            time.sleep(1)           
            print(ser.readline().decode('ascii'))
            ishandDetected=0


def drawHands():
    global val,dist,ishandDetected
    previousX=320
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            
            h,w,c=image.shape
            hc=h//2
            wc=w//2
            cv2.circle(image,(wc,hc),6,(255,0,0),cv2.FILLED)
            
            #print(h,w)
            if not success:
                print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # to get the list of points
            lmList=[]
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                myHand=results.multi_hand_landmarks[0]

                for id,lm in enumerate(myHand.landmark):
                    
                    cx,cy = int(lm.x*w),int(lm.y*h)

                    lmList.append([id,cx,cy])
                x1,y1 = lmList[0][1],lmList[0][2]
                x2,y2 = lmList[9][1],lmList[9][2]

                handcenterx,handcentery = (x1+x2)//2 , (y1+y2)//2
                            

                dist = previousX - handcenterx
                ishandDetected=1

                previousX = handcenterx
                image = cv2.flip(image, 1)
                cv2.putText(
                    image, #numpy array on which text is written
                    "Distance: "+str(dist), #text
                    (10,30), #position at which writing has to start
                    cv2.FONT_HERSHEY_SIMPLEX, #font family
                    1, #font size
                    (209, 80, 0, 255), #font color
                    3) #font stroke
                image = cv2.flip(image, 1)
                
                # if dist>0:
                #     i='1'
                # elif dist<0:
                #     i='2'

                cv2.line(image,(handcenterx,handcentery),(wc,hc),(0,0,255),5)

                cv2.circle(image,(handcenterx,handcentery),6,(0,255,0),cv2.FILLED)

            
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            

            key = cv2.waitKey(1)
            if key==ord("q"):
                val=1
                print("done")
                break


t1 =  threading.Thread(target = drawHands)
t2 =  threading.Thread(target = serial)

t1.start()
t2.start()

t1.join()
t2.join()



cap.release()

ser.close()
