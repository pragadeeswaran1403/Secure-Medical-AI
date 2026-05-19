import json

def get_patient_record(patient_id):

    with open("patient_records.json","r") as f:
        data = json.load(f)

    for record in data:

        if record["patient_id"] == patient_id:
            return record

    return None