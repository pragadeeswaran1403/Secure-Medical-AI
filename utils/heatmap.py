import cv2

def apply_heatmap(image):
    heat = cv2.applyColorMap(image, cv2.COLORMAP_JET)
    return cv2.addWeighted(image, 0.6, heat, 0.4, 0)