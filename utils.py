from djitellopy import Tello
import cv2 as cv
import numpy as np

def init_tello():
    myDrone=Tello()
    myDrone.connect()
    myDrone.for_back_velocity=0
    myDrone.left_right_velocity=0
    myDrone.up_down_velocity=0
    myDrone.yaw_velocity=0
    myDrone.speed=0
    battery_level = myDrone.get_battery()
    print(f"Battery is {battery_level}%")
    if battery_level < 20:
        raise Exception("Battery level too low to take off.")
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

def telloGetFrame(myDrone, w=360,h=240):
    img=myDrone.get_frame_read().frame
    img=cv.resize(img,(w,h))
    img=cv.cvtColor(img, cv.COLOR_BGR2RGB)
    return img

def findFace(img):
    faceCascade=cv.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(imgGray,1.2,4)
    myFaceListC=[]
    myFaceListArea=[]
    for(x,y,w,h) in faces:
        cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cx=x+w//2
        cy=y+h//2
        area=w*h
        myFaceListArea.append(area)
        myFaceListC.append([cx,cy])
    
    if len(myFaceListArea)!=0:
        i=myFaceListArea.index(max(myFaceListArea))
        return img,(myFaceListC[i],myFaceListArea[i] )
    else:
        return img,[[0,0],0]
    
    
def trackFace(myDrone,info,w,pid,pError):
    ##PID
    error=info[0][0]- w//2
    speed=pid[0]*error+pid[1]*(error-pError)
    speed=int(np.clip(speed, -100,100))
    if info[0][0]!=0:
        myDrone.yaw_velocity=speed
    else:
        myDrone.yaw_velocity=0
        myDrone.for_back_velocity=0
        myDrone.left_right_velocity=0
        myDrone.up_down_velocity=0
        error=0
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
    return error
