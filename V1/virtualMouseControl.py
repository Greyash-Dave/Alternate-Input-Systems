import cv2
import numpy as np
import HandTrackingModule as htm
import mouseInputField as mif
import time
import pyautogui

def gesture_mouse():
    #16:9
    wCam, hCam = mif.wCam, mif.hCam
    windowName = "GestureMouse"
    wScr, hScr = pyautogui.size()

    pTime = 0
    pLocX, pLocY = 0, 0
    cLocX, cLocY = 0, 0
    smoothening  = 5
    staticIdScale = 40
    onclick = False
    onclickCounter = -1
    cursorMode = False
    counterCursorMode = 0
    mode = "Capture"

    field = mif.topAllignField

    detector = htm.handDetector(maxHands=1)

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    Run = True

    # blackScreen = np.zeros((hCam, wCam))

    while Run:
        success, img = cap.read()
        img = detector.findHands(img)
        height, width, channels = img.shape
        lmList, bbox = detector.findPosition(img)
        # print(height, width)

        cv2.rectangle(img, field[0], field[1], (255, 0, 255), thickness=2)

        if len(lmList)!=0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[4][1:]

            # print(x2-x1)

            fingers = detector.fingersUp()
            #print(fingers)

            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[0] == 0 and fingers[4] == 1:
                cursorMode = True
                mode = "Cursor"

            if fingers[1] == 0 and fingers[2] == 1 and fingers[4] == 1 and fingers[0] == 0 and fingers[3] == 1:
                cursorMode = False
                mode = "Capture"
            
            if  cursorMode:
                if fingers[1] == 1 and fingers[0] == 1 and (x2-x1>20 or x1-x2>20):
                    x3 = np.interp(x1, (0, wCam), (0, wScr))
                    y3 = np.interp(y1, (0, hCam), (0, hScr))
                    if (field[0][0]<x1 and x1<(field[1][0])) and (field[0][1]<y1 and y1<(field[1][1])):
                        x3 = np.interp(x1, (field[0][0], field[1][0]), (0, wScr))
                        y3 = np.interp(y1, (field[0][1], field[1][1]), (0, hScr))
                        pyautogui.moveTo(wScr-x3, y3)
                        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    else:
                        try:
                            obj = mif.closeFieldLine(field, [x1, y1])
                            if isinstance(obj, tuple):
                                x1, y1 = obj

                            else:
                                line1 = obj
                                line2=[[x1, y1], [(field[0][0]+field[1][0])/2, (field[0][1]+field[1][1])/2]]
                                x1, y1 = mif.line_intersection(line1, line2)
                                x1, y1 = int(x1), int(y1)
                            x3 = np.interp(x1, (field[0][0], field[1][0]), (0, wScr))
                            y3 = np.interp(y1, (field[0][1], field[1][1]), (0, hScr))
                            #print(x3, y3)

                            # if 0<(cLocX-pLocX)<staticIdScale or 0>(cLocX-pLocX)>staticIdScale:
                            #     cLocX = pLocX
                            #     cLocY = pLocY
                            # else:
                            #     cLocX = pLocX + (x3-pLocX)/smoothening
                            #     cLocY = pLocY + (y3-pLocY)/smoothening
                            cLocX = pLocX + (x3-pLocX)/smoothening
                            cLocY = pLocY + (y3-pLocY)/smoothening

                            pyautogui.moveTo(wScr-cLocX, cLocY)
                            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                            #print(cLocX, cLocY)
                            pLocX, pLocY = cLocX, cLocY
                        except Exception as e:
                            print(e)
                if (fingers[1] == 1 and fingers[0] == 0) and (x2-x1<20 or x1-x2<20) and not onclick:
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()
                    onclick = True
                    onclickCounter += 1
                    # length, img, _ = detector.findDistance(8, 12, img)
                    # #print(length)
                    # if length < 40:
                    #     cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    #     pyautogui.click()
                if fingers[1] == 1 and fingers[0] == 1:
                    onclick = False
                if onclick and onclickCounter==0:
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()
                    onclick =False

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.putText(img, mode, (20, 75), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow(windowName, img)
        #cv2.resizeWindow(windowName, wCam, hCam)
        cv2.waitKey(1)

        if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) <1:
            print(f"Closing {windowName} window")
            Run = False
    print("Exiting Virtual Mouse")

if __name__ == '__main__':
    gesture_mouse()