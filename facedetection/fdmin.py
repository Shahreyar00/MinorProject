import cv2 as cv 
import mediapipe as mp 
import time 

cap = cv.VideoCapture(0)
pTime = 0 

mpFaceDetection = mp.solutions.face_detection 
faceDetection = mpFaceDetection.FaceDetection(0.75)
mpDraw = mp.solutions.drawing_utils 

while True:
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    print(results)

    if results.detections:
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box 
            ih, iw, ic = img.shape 
            bbox = int(bboxC.xmin*iw), int(bboxC.ymin*ih), int(bboxC.width*iw), int(bboxC.height*ih)
            cv.rectangle(img, bbox, (255,0,255),2)
            cv.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0],bbox[1]-20), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime 

    cv.putText(img, f'FPS:{int(fps)}', (20,60), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    cv.imshow("Image", img)
    cv.waitKey(1)

