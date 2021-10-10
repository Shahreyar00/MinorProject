import cv2 as cv 
import mediapipe as mp 
import time 
import htmodule2 as htm 

cap = cv.VideoCapture(0)

pTime = 0
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) !=0:
        print(lmList[3])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime 

    cv.putText(img, str(int(fps)), (10,60), cv.FONT_HERSHEY_PLAIN, 2, (255,234,255), 2)

    cv.imshow("Image", img)
    cv.waitKey(1)

