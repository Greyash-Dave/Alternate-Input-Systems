# import cv2
# import numpy as np
# import HandTrackingModule as htm
# import time
# import numpy
# import socket

# wCam, hCam = 640, 480
# windowName = "fBirdInput"

# cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)

# detector = htm.handDetector(maxHands=1)

# s = socket.socket()
# print("Flappy Server Created")

# s.bind(("localhost", 9999))

# s.listen(1)
# print("Waiting For Connection")

# RUN = True
# fBirdJumpClick = "False"
# playMode = "False"

# thumbCollisionList = []

# def thumbCollidePosition(prediction):
#     pass

# while RUN:

#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList, bbox = detector.findPosition(img)

#     if len(lmList) != 0:
#         try:
#             c, addr = s.accept()
#             print("Connected To Client", addr)
#         except:
#             addr = False


#         x1, y1 = lmList[4][1:]
#         x2, y2 = lmList[6][1:]
#         #print(y2-y1)

#         fingers = detector.fingersUp()
#         #print(fingers)

#         if y2-y1 > 40:
#             fBirdJumpClick = "False"
#         else:
#             fBirdJumpClick = "True"
        
#         if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
#             playMode = "True"
#         else:
#             playMode = "False"
        
#         if addr != False:
#             pass

#         c.send(bytes(fBirdJumpClick+","+playMode, "utf-8"))

#         c.close()

#         #print(fBirdJumpClick)

#     cv2.imshow(windowName, img)
#     cv2.waitKey(1)

#     if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) <1:
#         print(f"Closing {windowName} window")
#         RUN = False
#         quit()
#print("Exiting Virtual Mouse")


import cv2
import numpy as np
import HandTrackingModule as htm
import time
import numpy
import socket


wCam, hCam = 640, 480
windowName = "fBirdInput"
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)

UDP_IP = "127.0.0.1"  # Replace with your Unity IP address
UDP_PORT = 5000       # Replace with the Unity port number

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Created Server")

RUN = True
fBirdJumpClick = "False"
playMode = "False"

sockName = "camInputClient"

# c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# c.connect(("localhost", 9999))

playModeOn, fBirdJumpClickOn = False, False
pTime = 0

while RUN:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        sensing = True

        try:
            x1, y1 = lmList[0][4][1:]
            x2, y2 = lmList[0][6][1:]
        except:
            x1, y1 = lmList[4][1:]
            x2, y2 = lmList[6][1:]
        #print(y2-y1)

        fingers = detector.fingersUp()
        #print(fingers)

        if y2-y1 < 40:
            if fBirdJumpClickOn != True:
                fBirdJumpClick = "True"
                fBirdJumpClickOn = True
            else:
                fBirdJumpClick = "False"

        else:
            fBirdJumpClick = "False"
            fBirdJumpClickOn = False
        
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
            if playModeOn != True:
                playMode = "True"
                playModeOn = True
            else:
                playMode = "False"
        else:
            playMode = "False"
            playModeOn = False
        
        # if addr != False:
        #     pass

        #print(fBirdJumpClick, playMode)



        try:
            data = fBirdJumpClick+","+playMode
            sock.sendto(bytes(data, 'utf-8'), (UDP_IP, UDP_PORT))
        except Exception as e :
            print(e)

        #print(fBirdJumpClick)
        pPlayMode = playMode
        pFBirdJumpClick = fBirdJumpClick
    else: 
        sensing = False


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, "Hand Tracking UI", (195, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(img, "FPS:"+str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    cv2.putText(img, ("Tracking:"+str(sensing)), (20, 78), cv2.FONT_HERSHEY_PLAIN, 2, (237, 71, 255), 2)
    cv2.putText(img, fBirdJumpClick+","+playMode, (525, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 3)

    cv2.imshow(windowName, img)
    cv2.waitKey(1)

    if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) <1:
        print(f"Closing {windowName} window")
        RUN = False
        quit()
print("Exiting Virtual Mouse")

