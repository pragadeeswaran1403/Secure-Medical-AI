import numpy as np
import cv2

def classify_scan(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # brightness
    avg = np.mean(gray)

    # edges (important for bone)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges) / (gray.shape[0] * gray.shape[1])

    # decision logic
    if edge_density > 20:
        return "Bone Scan"

    elif avg < 90:
        return "Brain MRI"

    else:
        return "Chest Scan"