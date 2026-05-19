import os
import cv2
import numpy as np

# dataset paths
BRAIN_PATH = "dataset/brain_tumor_dataset"
CHEST_PATH = "dataset/chest_xray_dataset"
BONE_PATH = "dataset/bone_fracture_dataset"

IMG_SIZE = 224

def load_images(folder, label):
    data = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        img = cv2.imread(path)
        if img is None:
            continue
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        data.append((img, label))
    return data

def load_dataset():
    data = []

    # brain
    data += load_images(os.path.join(BRAIN_PATH, "yes"), 1)
    data += load_images(os.path.join(BRAIN_PATH, "no"), 0)

    # chest
    data += load_images(os.path.join(CHEST_PATH, "PNEUMONIA"), 1)
    data += load_images(os.path.join(CHEST_PATH, "NORMAL"), 0)

    # bone
    data += load_images(os.path.join(BONE_PATH, "fracture"), 1)
    data += load_images(os.path.join(BONE_PATH, "normal"), 0)

    X = np.array([i[0] for i in data]) / 255.0
    y = np.array([i[1] for i in data])

    return X, y

def predict_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0

    mean = np.mean(img)

    if mean > 0.6:
        return "Abnormal Detected", 0.9
    else:
        return "Normal", 0.8