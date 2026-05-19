import os
from datetime import datetime

LOG_FILE = "access_log.txt"

def log_access(doctor, patient):

    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    log = f"{doctor} viewed {patient} at {time}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log)

def get_logs():

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        return f.readlines()