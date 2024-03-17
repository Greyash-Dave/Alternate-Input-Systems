import cv2
import numpy as np
from modules import HandTrackingModule as htm
from modules import mouseInputField as mif
import time
import pyautogui

def gesture_mouse():
    #16:9
    wCam, hCam = mif.wCam, mif.hCam
    windowName = "GestureMouse"
    wScr, hScr = pyautogui.size()

    pTime = 0

    detector = htm.handDetector(maxHands=1)

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    Run = True

    while Run:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        if len(lmList)!=0:
            x1, y1 = lmList[4][1:]

            fingers = detector.fingersUp()

            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[0] == 0 and fingers[4] == 1:
                cursorMode = True
                mode = "Cursor"

            if fingers[1] == 0 and fingers[2] == 1 and fingers[4] == 1 and fingers[0] == 0 and fingers[3] == 1:
                cursorMode = False
                mode = "Capture"

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
    
        cv2.imshow(windowName, img)

        cv2.waitKey(1)

        if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) <1:
            print(f"Closing {windowName} window")
            Run = False
    print("Exiting Virtual Mouse")

if __name__ == '__main__':
    gesture_mouse()