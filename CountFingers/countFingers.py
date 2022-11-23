import cv2
import time
import os
import handTracking_module as htm

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "fingerImgs"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
pTime = 0

detector = htm.hand_detector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findhands(img)
    lmList = detector.findPosition(img, draw = False)

    if len(lmList)!= 0:
        fingers = [] 
        #thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
            #fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0) 
        #print(fingers)

        totalFingers = fingers.count(1)
        print(totalFingers)

        img[0:200,0:200] = overlayList[totalFingers-1]

        cv2.rectangle(img, (20, 255), (170,425), (0, 255,0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45,375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0,0),25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}',(400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    cv2.imshow("img", img)
    key = cv2.waitKey(1)
    if key==81 or key==113:
        break