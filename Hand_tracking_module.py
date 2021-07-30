import cv2 as cv
import mediapipe as mp
import time


cap = cv.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands() # here write parameters # this object only takes RGB images
mpdraw = mp.solutions.drawing_utils # this is used to draw the 21 utility points of the hand tracking module
previous_time = 0
current_time = 0

while True:
    success, image = cap.read()
    
    
    imageRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(imageRGB) # this process the frames for us
    #print(results.multi_hand_landmarks) # by this process we can read information of hands

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id, land_mark in enumerate(handlms.landmark): # id is for each corresponding point, land_mark give the x,y,z coordinates of each point
                #print(id, land_mark)
                height, width, channel = image.shape
                cx, cy = int(land_mark.x*width) , int(land_mark.y * height) # here we have converted the x,y coordinates to pixel coordinates.
                print(id, cx, cy)   
                
                
                cv.circle(image, (cx,cy), 10, (255,0,255), cv.FILLED)

            mpdraw.draw_landmarks(image, handlms, mphands.HAND_CONNECTIONS) # used this to draw the 21 point and connect them via lines.
            

    current_time = time.time()
    fps = 1/(current_time - previous_time)

    previous_time = current_time

    cv.putText(image, str(int(fps)),(10,70), cv.FONT_HERSHEY_COMPLEX, 2,(0,0,255),3)

    cv.imshow('image', image)
    cv.waitKey(1)

