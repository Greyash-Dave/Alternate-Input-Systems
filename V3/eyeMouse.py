import cv2
import mediapipe as mp
import pyautogui
import numpy as np

cap = cv2.VideoCapture(0)

RUN = True
windowName = "eM UI"
scrW, scrH = pyautogui.size()

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

print("Starting EYE MOUSE")

while RUN:

    _, frame = cap.read()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)

    landmarks_points = output.multi_face_landmarks

    winH, winW, _ = frame.shape

    # print(landmarks_points)
    if landmarks_points:
        landmarks = landmarks_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * winW)
            y = int(landmark.y * winH)
            cv2.circle(frame, (x, y), 3, (255, 0, 0))
            if id ==1:
            #     x = (scrW/winW) * x
            #     y = (scrH/winH) * y
                x = np.interp(x, (0, winW), (0, scrW))
                y = np.interp(y, (0, winH), (0, scrH))
                pyautogui.moveTo(x, y)

                    

    cv2.imshow(windowName, frame)
    cv2.waitKey(1)

    if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) <1:
            print(f"Closing {windowName} window")
            RUN = False