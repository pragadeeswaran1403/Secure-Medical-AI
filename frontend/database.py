import json
import os

DB_FILE = "patients.json"

# ---------------- LOAD DB ----------------
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

# ---------------- SAVE DB ----------------
def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- ADD RECORD ----------------
from datetime import datetime

def add_patient_record(patient_id, ipfs_hash, tx_id, scan_type, risk,doctor,date):
    db = load_db()

    if patient_id not in db:
        db[patient_id] = []
        
        db[patient_id].append({
        "ipfs_hash": ipfs_hash,
        "transaction": tx_id,
        "scan": scan_type,
        "risk": risk,
        "doctor": doctor,
        "date": str(datetime.now())
        })

    save_db(db)

# ---------------- GET RECORDS ----------------
def get_patient_records(patient_id):
    db = load_db()

    # 🔥 ALL records fetch (Admin use)
    if patient_id == "all":
        all_records = []
        for pid, records in db.items():
            for r in records:
                all_records.append({
                    "pid": pid,
                    "ipfs_hash": r["ipfs_hash"],
                    "transaction": r["transaction"]
                })
        return all_records

    # 👤 single patient
    return db.get(patient_id, [])

# ---------------- DELETE RECORD ----------------
def delete_record(pid):
    db = load_db()

    if pid in db:
        del db[pid]

    save_db(db)

# ---------------- STATS ----------------
def get_stats():
    db = load_db()
    total_patients = len(db)
    total_records = sum(len(v) for v in db.values())
    return total_patients, total_records