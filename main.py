from discordrp import Presence
import time

import os
import glob
import json

def load(logDir):
    print("Parsing log file")
    log_files = glob.glob(os.path.join(logDir, '*.log'))
    latest_file = max(log_files, key=os.path.getmtime)
    print("opening log file " + str(latest_file))
    res = []
    with open(latest_file) as f:
        for line in f:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Skip empty lines
                try:
                    data = json.loads(line)
                    res.append(data)
                except json.JSONDecodeError:
                    print(f"Skipping line: {line}")
    return res

def getCMDR(logs):
    print("Parsing log data")
    with open("messages.json") as m:
        messages = json.load(m)
    for log in logs:
        if "event" in log:
            #print(log["event"])
            try:
                if log["event"] == "Commander":
                    cmdr_name = log.get("Name", "")
                    print(f"Found commander: {cmdr_name}")
            except Exception:
                print("No commander found")
    return cmdr_name

client_id = "1170388114498392095"  # Replace this with your own client id

with Presence(client_id) as presence:
    print("Connected")
    cmdr = getCMDR(load("C:/Users/Nicey/Saved Games/Frontier Developments/Elite Dangerous"))
    presence.set(
        {
            "state": "Playing as CMDR " + cmdr,
            "details": "Playing Elite: Dangerous",
            "timestamps": {
                "start": int(time.time()),
            },
            "assets": {
                "large_image": "ed_main",  # Replace this with the key of one of your assets

            },

            
        }
    )
    print("Presence updated")

    while True:
        time.sleep(15)