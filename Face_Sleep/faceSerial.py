import threading
import cv2
# import serial
import time

from pygame import mixer
import os

absolute_path = os.path.dirname(__file__)
#relative_path = "src/lib"
full_path_meme = absolute_path + "\meme.jpg"
# Starting the mixer

# ser=serial.Serial(port="COM3",baudrate=9600)
# ser.timeout=1
path = full_path_meme
image = cv2.imread(path)

face_detector = cv2.CascadeClassifier(
        f"{cv2.data.haarcascades}haarcascade_frontalface_default.xml")
eye_detector = cv2.CascadeClassifier(
        f"{cv2.data.haarcascades}haarcascade_eye.xml")

video = cv2.VideoCapture(0)

isEyesDetected = True
forceStop = False

def serial():
    global isEyesDetected,forceStop
    while True:
        if forceStop==True:
            break
        if isEyesDetected == False:
            mixer.init()
  
            # Loading the song
            mixer.music.load("wakeup1.mp3")
            
            # Setting the volume
            mixer.music.set_volume(0.7)
            mixer.music.play()
            cv2.imshow("wakeup",image)
            cv2.waitKey(1000)
            mixer.music.stop()
            cv2.destroyWindow("wakeup")
            isEyesDetected = True
            # playsound('audio.mp3')
            # ser.write(isEyesDetected.encode())
            # print(ser.readline().decode('ascii'))


def faceTracking():
    global isEyesDetected,forceStop
    while True:
        ret, frame = video.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_points = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in face_points:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 20), 2)
        
            face = frame[y:y+h,x:x+w]
            eyes = eye_detector.detectMultiScale(face,1.3,5)
            print(len(eyes))
            if len(eyes)==0 and len(face_points)>0:
                isEyesDetected = False

            print("**************************************")

            for (x, y, w, h) in eyes:
                cv2.rectangle(face, (x, y), (x+w, y+h), (155, 0, 120), 2)


        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            forceStop = True
            break

t1 =  threading.Thread(target = faceTracking)
t2 =  threading.Thread(target = serial)

t1.start()
t2.start()

t1.join()
t2.join()


cv2.destroyAllWindows()
video.release()

