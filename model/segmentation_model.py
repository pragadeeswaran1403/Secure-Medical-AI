import cv2
import numpy as np

def segment_tumor(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # better segmentation
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    _, thresh = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY)

    # mask overlay
    mask = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    result = cv2.addWeighted(img, 0.7, mask, 0.3, 0)

    return result