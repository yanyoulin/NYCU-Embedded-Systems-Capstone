#!/usr/bin/python3

import sys
import cv2 
import time
import math
import numpy as np
import mediapipe as mp
import imutils

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
mp_drawing = mp.solutions.drawing_utils 


def detectPose(image, pose):
    output_image = image.copy()
    
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    
    height, width, _ = image.shape
    landmarks = []
    
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)
        
        for landmark in results.pose_landmarks.landmark:
            
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))
    
    return output_image, landmarks


def calculateAngle(landmark1, landmark2, landmark3):
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    if angle < 0:
        angle += 360

    angle = min(angle, 360 - angle)
    
    return angle


def classifyPose(landmarks, output_image):
    label = 'Unknown Pose'

    color = (0, 0, 255)
    
    #----------------------------------------------------------------------------------------------------------------
    # Calculate the required angles.
    #----------------------------------------------------------------------------------------------------------------
    
    try:
        # Get the angle between the left shoulder, elbow and wrist points. 
        left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    
        # Get the angle between the right shoulder, elbow and wrist points. 
        right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
    
        # Get the angle between the left elbow, shoulder and hip points. 
        left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                             landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

        # Get the angle between the right hip, shoulder and elbow points. 
        right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

        # Get the angle between the left hip, knee and ankle points. 
        left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

        # Get the angle between the right hip, knee and ankle points 
        right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    
        #----------------------------------------------------------------------------------------------------------------
        # Check if it is the warrior II pose
        #----------------------------------------------------------------------------------------------------------------
    
        print("=======================================")
        # 1. Check if the both arms are straight.
        print("left_elbow_angle:", int(left_elbow_angle))
        print("right_elbow_angle:", int(right_elbow_angle))
        if 165 < left_elbow_angle < 195 and 165 < right_elbow_angle < 195:
            print("# 1. Both arms are straight")
            print("=======================================")

            print("left_shoulder_angle:", int(left_shoulder_angle))
            print("right_shoulder_angle:", int(right_shoulder_angle))
            # 2. Check if shoulders are at the required angle.
            if 80 < left_shoulder_angle < 110 and 80 < right_shoulder_angle < 110:
                print("# 2. Shoulders are at the required angle")
                print("=======================================")

                print("left_knee_angle:", int(left_knee_angle))
                 # 3. Check if one leg is straight.
                if 165 < left_knee_angle < 195:
                    print("# 3. One leg is straight")
                    print("=======================================")

                    # 4. Check if the other leg is bended at the required angle.
                    print("right_knee_angle", int(right_knee_angle))
                    if 90 < right_knee_angle < 120:
                        print("# 4. The other leg is bended at the required angle")
                        print("=======================================")

                        # Specify the label of the pose that is Warrior II pose.
                        label = 'Warrior II Pose' 
                if 165 < right_knee_angle < 195:
                    print("# 3. One leg is straight")
                    print("=======================================")

                    # 4. Check if the other leg is bended at the required angle.
                    print("right_knee_angle", int(right_knee_angle))
                    if 90 < left_knee_angle < 120:
                        print("# 4. The other leg is bended at the required angle")
                        print("=======================================")

                        # Specify the label of the pose that is Warrior II pose.
                        label = 'Warrior II Pose' 
    except:
        output_image = []

    
    return output_image, label


def main():
    try:
        image = cv2.imread(sys.argv[1])
    except:
        image = cv2.imread("warrior-pose.jpg")

    pose_image, landmarks = detectPose(image, pose)
    output_image, label = classifyPose(landmarks, pose_image)

    if label != 'Unknown Pose':
        color = (0, 255, 0)  
    else:
        color = (0, 0, 255)

    cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    cv2.imshow('Pose Detection', output_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


