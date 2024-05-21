from utils import *
import cv2 as cv

w,h=360,240
pid=[0.5,0.5,0]
pError=0
myDrone=init_tello()
startCounter = 0  # For no flight put this as "1". For flight put this on "0"

while True:
    # Flight
    if startCounter == 0:
        print("Attempting to take off...")
        try:
            myDrone.takeoff()
            print("Takeoff successful!")
            startCounter = 1
        except Exception as e:
            print(f"Takeoff failed: {e}")
            break
    #step 1:
    img=telloGetFrame(myDrone)  
    #step 2:
    img,info=findFace(img)
    print(info[0][0])
    #step 3:
    pError=trackFace(myDrone,info,w,pid,pError)
    cv.imshow("img", img)
    if cv.waitKey(1) & 0xFF==ord("q"):
        myDrone.land()
        break
