import cv2
import numpy as np

def detect_tumor(image_path):

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    _,thresh = cv2.threshold(blur,45,255,cv2.THRESH_BINARY)

    contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:

        if cv2.contourArea(c) > 500:

            x,y,w,h = cv2.boundingRect(c)

            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imwrite("tumor_detected.jpg",img)

    return "tumor_detected.jpg"