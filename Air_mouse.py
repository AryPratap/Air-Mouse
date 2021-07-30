import cv2 as cv
import Hand_Tracking as htm
import numpy as np
import time
import pyautogui
#height and width of cam
wCam = 640 
hCam = 480
# Capturing video and getting dimensions of window
cap = cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
cTime = 0
detector = htm.hand_detector(maxHand=1)
wScr, hScr = pyautogui.size()
frameR = 100
# Initializing smoothening values
smooth = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0


while True:
    # reading image
    success, img = cap.read()

    # Finding Landmark
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Getting coordinates of tip of index and middle finger
    if len(lmList)!= 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        print(x1, y1, x2, y2)

    # Checking which fingers are up
    fingers = detector.fingersUp()
    print(fingers)
    cv.rectangle(img, (frameR,frameR), (wCam-frameR, hCam - frameR), (255,0,255), thickness=3)

    # if only index finger is up, then mouse in moving mode
    if len(fingers)!=0:
        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:

        # Converting Coordinates
            x3 = np.interp(x1, (frameR,wCam-frameR), (0,wScr))
            y3 = np.interp(y1, (frameR,hCam-frameR), (0,hScr))

        # smoothening values
            clocX = plocX + (x3-plocX)/smooth
            clocY = plocY + (y3-plocY)/smooth

        # move mouse
            pyautogui.moveTo(wScr - clocX,clocY, duration=0.005)
            cv.circle(img, (x1,y1),10, (255,0,255), cv.FILLED)
            plocX, plocY = clocX, clocY

        # clicking mode, both fingers up  
        if fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0 and fingers[0]==0:
            # finding distance between index and middle finger
            length, img, lineInfo = detector.findDistance(8,12,img)
            print(length)
        # clicking command
            if length<35:
                cv.circle(img, (lineInfo[4], lineInfo[5]), 10, (0,255,0),cv.FILLED)          
                pyautogui.click()    
            
        # scroll up when index and smallest finger up, rest all fingers down
        if fingers[4]==1 and fingers[1]==1 and fingers[0]==0 and  fingers[2]==0 and fingers[3]==0:
        
            pyautogui.scroll(200)

        # scroll down when only smallest finger up, rest all fingers down
        if fingers[4]==1 and fingers[1]==0 and fingers[0]==0 and  fingers[2]==0 and fingers[3]==0:

            pyautogui.scroll(-200)
        # press space bar when only thumb up, rest all fingers down    
        if fingers[0]==1 and fingers[1]==0 and  fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
            pyautogui.typewrite(['space'])
    # Frame Rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (10,50),  cv.FONT_HERSHEY_COMPLEX, 2,(0,0,255),3)


    # Display
    cv.imshow('img', img)
    cv.waitKey(1)
   



