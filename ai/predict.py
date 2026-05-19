import numpy as np
import cv2

def preprocess(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (224,224))
    img = img / 255.0
    img = np.reshape(img, (1,224,224,3))
    return img

def predict_brain(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY)

    contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    tumor = False
    area_total = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            tumor = True
            area_total += area
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

    confidence = min(95, 60 + (area_total/1000))

    if tumor:
        return "Tumor Detected", confidence, img
    else:
        return "No Tumor", confidence, img