import json
import os
import glob
import getpass

global username
username = getpass.getuser()

global eventAssociationsMain
global eventAssociationsDocked
global eventAssociationsCombat
eventAssociationsMain = {"SupercruiseEntry":"Supercrusing in ", "SupercruiseExit":"Flying in ", "FSDJump":"Jumping to ", "FSSSignalDiscovered": "In Supercruse", "Undocked": "Flying in "}
eventAssociationsDocked = {"Touchdown":"Landed on ", "Docked": "Docked at ","DockingGranted": "Docked at "}
eventAssociationsCombat = {"UnderAttack": "In a fight!"}

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
    cmdr_name = "CMDR"
    for log in logs:
        if "event" in log:
            try:
                if log["event"] == "Commander":
                    cmdr_name = log.get("Name", "")
                    print(f"Found commander: {cmdr_name}")
            except Exception:
                print("No commander found")
    return cmdr_name

def getSystem(logs):
    print("Parsing log data - looking for system")
    j = 0
    for log in logs:
        j+1
        if "event" in log:
            try:
                if log["event"] == "Location":
                    system_name = log.get("StarSystem", "")
                    print(f"Found system: {system_name}")
                if log["event"] == "SupercruiseEntry":
                    system_name_2 = log.get("StarSystem", "")
                    print(f"Found system: {system_name}")
            except Exception:
                print("No system found")
    if system_name == system_name_2:
        return system_name
    else:
        return system_name_2
    
def getStation(logs):
    print("Parsing log data - looking for station")
    for log in logs:
        if "event" in log:
            try:
                if log["event"] == "Location":
                    station_name = log.get("StationName", "")
                    print(f"Found station: {station_name}")
            except Exception:
                print("No station found")
    return station_name

def eventHandler(event):
    print("Parsing log data - looking for events")
    if event == "Shutdown":
        return "0"
    if event in eventAssociationsMain:
        if eventAssociationsMain[event] == "Fileheader":
            print("Fileheader found, skipping")
        else:
            print(f"Found event: {event}")
            system = getSystem(load("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous"))
            if system:  # Check if the string exists
                return eventAssociationsMain[event] + system
            else:
                return eventAssociationsMain[event]
    elif event in eventAssociationsDocked:
        station = getStation(load("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous"))
        if station:  # Check if the string exists
            print(f"Returning: {eventAssociationsDocked[event] + station}")
            return eventAssociationsDocked[event] + station
        else:
            return eventAssociationsDocked[event]
    else:
        print(f"Unknown event: {event}")
        return "Playing Elite: Dangerous"