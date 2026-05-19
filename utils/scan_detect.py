def detect_scan(name):
    name = name.lower()

    # Brain keywords
    if any(word in name for word in ["brain", "mri", "tumor"]):
        return "Brain MRI"

    # Chest keywords
    elif any(word in name for word in ["chest", "lung", "thorax"]):
        return "Chest Scan"

    # Bone keywords
    elif any(word in name for word in ["bone", "xray", "fracture"]):
        return "Bone Scan"

    # Default
    else:
        return "Unknown"