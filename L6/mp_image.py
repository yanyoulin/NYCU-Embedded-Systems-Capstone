#!/usr/bin/python3

import cv2
import sys
import time
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)

try:
    image = cv2.imread(sys.argv[1])
except Exception as e:  
    print(e)
    image = cv2.imread("images/warrior-pose.jpg")

output_image = image.copy()
imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pose.process(imageRGB)
height, width, _ = image.shape

landmarks = []

# Check if any landmarks are detected.
if results.pose_landmarks:

    # Draw Pose landmarks on the output image.
    mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
        connections=mp_pose.POSE_CONNECTIONS)
        
    # Iterate over the detected landmarks.
    for landmark in results.pose_landmarks.landmark:
            
        # Append the landmark into the list.
        landmarks.append((int(landmark.x * width), int(landmark.y * height),
            (landmark.z * width), landmark.visibility))


for idx, landmark in enumerate(landmarks):
    print("======================")
    print(idx, mp_pose.PoseLandmark(idx).name, landmark)

cv2.imshow("preview", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()




