from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
from scipy.spatial import distance as dist

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# 初始化
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("model/shape_predictor_68_face_landmarks.dat")

image = cv2.imread("img.png")
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

rects = detector(gray, 1)

for (i, rect) in enumerate(rects):
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    # 抓左眼與右眼
    leftEye = shape[43:48]
    rightEye = shape[37:42]
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    ear = (leftEAR + rightEAR) / 2.0

    # 顯示 EAR 值
    cv2.putText(image, "EAR: {:.2f}".format(ear), (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # 如果低於門檻值則顯示 DROWSY
    if ear < 0.25:
        cv2.putText(image, "DROWSY", (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

    # 顯示 landmark 點
    for (x, y) in shape:
        cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

cv2.imwrite("output.png", image)
print("Saved result to output.png")
