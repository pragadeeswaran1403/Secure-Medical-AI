from roi.roi_extraction import extract_roi

roi,bg = extract_roi("dataset/brain_tumor_dataset/yes/y1.jpg")

print("ROI Extracted")