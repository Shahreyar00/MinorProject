import cv2 as cv 
import time 
import numpy as np 
import math 
import htmodule as htm 

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#####
wCam, hCam = 640, 488
#####

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

valRange = volume.GetVolumeRange()

minVol = valRange[0]
maxVol = valRange[1]

vol = 0 
volBar = 400 
volPer = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        #print(lmList[4], lmList[8])

        x1,y1 = lmList[4][1], lmList[4][2]
        x2,y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv.circle(img, (x1,y1), 7, (255,0,255), cv.FILLED)
        cv.circle(img, (x2,y2), 7, (255,0,255), cv.FILLED)
        cv.line(img, (x1,y1), (x2,y2), (255,0,255), 2)
        cv.circle(img, (cx,cy), 7, (255,0,255), cv.FILLED)

        length = math.hypot(x2-x1, y2-y1)



        vol = np.interp(length, [20,60], [minVol, maxVol])
        volBar = np.interp(length, [20,120], [400,150])
        volPer = np.interp(length, [20,160], [0,100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<30:
            cv.circle(img, (cx,cy), 7, (0,255,0), cv.FILLED)

    cv.rectangle(img, (50,150), (85,400), (0,255,0))
    cv.rectangle(img, (50,int(volBar)), (85,400), (0,255,0), cv.FILLED)
    cv.putText(img,f'Vol:{int(volPer)}',(40,450), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime 

    cv.putText(img, f'FPS: {int(fps)}',(40,50), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    cv.imshow("Image", img)
    cv.waitKey(1)



