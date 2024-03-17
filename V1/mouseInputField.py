import cv2
import pyautogui

wCam, hCam = 640, 480
windowName = "GestureMouse"
wScr, hScr = pyautogui.size()
algnW = 100
algnH = 100
mouseInFieldSize = [320, 180]
mouseInFieldMidPos = [[int((wCam/2)-(mouseInFieldSize[0]/2)), int((hCam/2)-(mouseInFieldSize[1]/2))], [int((wCam/2)+(mouseInFieldSize[0]/2)), int((hCam/2)+(mouseInFieldSize[1]/2))]]
leftAllignField = [[mouseInFieldMidPos[0][0]-algnW, mouseInFieldMidPos[0][1]], [mouseInFieldMidPos[1][0]-algnW, mouseInFieldMidPos[1][1]]]
leftAllignFieldMid = leftAllignField[0][0]+mouseInFieldSize[0], leftAllignField[0][1]+mouseInFieldSize[1]
topAllignField = [[mouseInFieldMidPos[0][0], mouseInFieldMidPos[0][1]-algnH], [mouseInFieldMidPos[1][0], mouseInFieldMidPos[1][1]-algnH]]

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def closeFieldLine(field, pt):

    topLine =    [[field[0][0], field[0][1]], [field[1][0], field[0][1]]]
    bottomLine = [[field[0][0], field[1][1]], [field[1][0], field[1][1]]]
    leftLine =   [[field[0][0], field[0][1]], [field[0][0], field[1][1]]]
    rightLine =  [[field[1][0], field[0][1]], [field[1][0], field[1][1]]]

    def distLineToPoint(line):
        dist = ((line[1][0]-line[0][0])**2 + (line[1][1]-line[0][1])**2)**0.5
        return dist
    def midPoint(line):
        mid = [(line[0][0]+line[1][0])/2, (line[0][1]+line[1][1])/2]
        return mid

    # topMid = midPoint(topLine)
    # bottomMid = midPoint(bottomLine)
    # leftMid = midPoint(leftLine)
    # rightMid = midPoint(rightLine)

    minDis = wCam
    minDisLine = False
    ePoint=(None)
    detect=False

    # if distLineToPoint([topMid, pt]) < minDis:
    #     minDis = distLineToPoint([topMid, pt])
    #     minDisLine = topLine
    #     detect = "topLine"
    #     #print(distLineToPoint([topMid, pt]))
    
    # if distLineToPoint([bottomMid, pt]) < minDis:
    #     minDis = distLineToPoint([bottomMid, pt])
    #     minDisLine = bottomLine
    #     detect = "Line"
    
    # if distLineToPoint([leftMid, pt]) < minDis:
    #     minDis = distLineToPoint([leftMid, pt])
    #     minDisLine = leftLine
    #     detect = "leftLine"
    
    # if distLineToPoint([rightMid, pt]) < minDis:
    #     minDis = distLineToPoint([rightMid, pt])
    #     minDisLine = rightLine
    #     detect = "rightLine"
    # print(detect)

    if topLine[0][0]<pt[0]<topLine[1][0] and pt[1]<topLine[0][1]:
        minDisLine = topLine

    if bottomLine[0][0]<pt[0]<bottomLine[1][0] and pt[1]>bottomLine[0][1]:
        minDisLine = bottomLine

    if leftLine[0][1]<pt[1]<leftLine[1][1] and pt[0]<leftLine[0][0]:
        minDisLine = leftLine

    if rightLine[0][1]<pt[1]<rightLine[1][1] and pt[0]>rightLine[0][0]:
        minDisLine = rightLine
    
    if pt[0]>rightLine[0][0] and pt[1]<topLine[0][1]:
        ePoint = (rightLine[0][0], topLine[0][1])
    
    if pt[0]>rightLine[0][0] and pt[1]>bottomLine[0][1]:
        ePoint = (rightLine[0][0], bottomLine[0][1])

    if pt[0]<leftLine[0][0] and pt[1]<topLine[0][1]:
        ePoint = (leftLine[0][0], topLine[0][1])

    if pt[0]<leftLine[0][0] and pt[1]>bottomLine[0][1]:
        ePoint = (leftLine[0][0], bottomLine[0][1])

    if minDisLine:
        return minDisLine
    if ePoint:
        return ePoint
