def get_risk_level(scan_type):
    if scan_type == "Brain MRI":
        return "HIGH RISK ⚠️"
    elif scan_type == "Chest Scan":
        return "MEDIUM RISK ⚡"
    else:
        return "LOW RISK ✅"