from ultralytics import YOLO
import cv2
import time
import os

model = YOLO('yolov8n.pt')

img_path = 'wake.jpg'
img = cv2.imread(img_path)

if img is None:
    print(f"[ERROR] Cannot read image: {img_path}")
    exit()
model.predict(source=img, save=False, conf=0.5, verbose=False)

t_start = time.monotonic()
results = model.predict(source=img, save=True, save_txt=False, conf=0.5, verbose=False)
dt = time.monotonic() - t_start
print(f"[INFO] YOLOv8 time:{dt:.2f} sec")

boxes = results[0].boxes
names = model.names
confidences = boxes.conf
class_ids = boxes.cls.int()
rects = boxes.xyxy.int()