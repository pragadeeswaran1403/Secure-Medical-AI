import json
import os

DB_FILE = "patient_records.json"

def save_patient_record(patient_id, ipfs_hash, tx_id):

    record = {
        "patient_id": patient_id,
        "ipfs_hash": ipfs_hash,
        "transaction": tx_id
    }

    if os.path.exists(DB_FILE):

        with open(DB_FILE,"r") as f:
            data = json.load(f)

    else:
        data = []

    data.append(record)

    with open(DB_FILE,"w") as f:
        json.dump(data,f,indent=4)