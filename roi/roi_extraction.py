import cv2

def extract_roi(image_path, scan_type="brain"):

    img = cv2.imread(image_path)

    if img is None:
        return None, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Better preprocessing
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # EDGE DETECTION (works for all scans)
    edges = cv2.Canny(blur, 30, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:

        # biggest area contour
        c = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(c)

        roi = img[y:y+h, x:x+w]

        # draw rectangle
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)

        cv2.imwrite("roi.jpg", roi)
        cv2.imwrite("highlight.jpg", img)

        return roi, img

    # fallback
    cv2.imwrite("roi.jpg", img)
    cv2.imwrite("highlight.jpg", img)

    return img, img