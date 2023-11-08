import json
import os
import glob
import getpass

global username
username = getpass.getuser()

global journalPath
journalPath = (
    "C:/Users/" + username + "/Saved Games/Frontier Developments/Elite Dangerous"
)

cmdr_name = "CMDR"

global eventAssociationsMain
global eventAssociationsDocked
global eventAssociationsCombat
eventAssociationsMain = {
    "SupercruiseEntry": "Supercrusing in ",
    "SupercruiseExit": "Flying in ",
    "FSDJump": "Supercrusing in ",
    "FSSSignalDiscovered": "Supercrusing in ",
    "Undocked": "Flying in ",
}
eventAssociationsDocked = {
    "Touchdown": "Landed on ",
    "Docked": "Docked at ",
    "DockingGranted": "Docked at ",
}
eventAssociationsCombat = {"UnderAttack": "In a fight!"}


def load(logDir):
    """
    Loads the log file and returns it as a list.
    Accepts logDir as string.
    """
    print("Parsing log file")
    log_files = glob.glob(os.path.join(logDir, "*.log"))
    latest_file = max(log_files, key=os.path.getmtime)
    print("Opening log file " + str(latest_file))
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
    res.reverse()  # so that it will stop when at the latest event it recognizes
    return res


def getCMDR(logs):
    """
    Returns the commander name as a string.
    Accepts logs as a list. (array)
    """
    print("Parsing log data")
    logs.reverse()  # becuase we want the first one. Undoes line 34
    cmdr_name = " "
    for log in logs:
        if "event" in log:
            try:
                if log["event"] == "Commander":
                    cmdr_name = log.get("Name", "")
                    print(f"Found commander: {cmdr_name}")
                    return cmdr_name
            except Exception:
                print("No commander found")
                return "Unknown"


def getSystem(logs):
    """
    Returns the system name as a string.
    Accepts logs as a list. (array)
    """
    print("Parsing log data - looking for system")
    system_name = " "
    for log in logs:
        if "event" in log:
            try:
                if log["event"] == "Location":
                    system_name = log.get("StarSystem", "")
                    print(f"Found system: {system_name}")
                    return system_name  # because we start with the latest one, we can just return it straight away 
                if log["event"] == "FSDJump":
                    system_name = log.get("StarSystem", "")
                    print(f"Found system: {system_name}")
                    return system_name
            except Exception:
                print("No system found")
                return "Unknown system"


def getStation(logs):
    """
    Returns the station name as a string.
    Accepts logs as a list. (array)
    """
    print("Parsing log data - looking for station")
    for log in logs:
        if "event" in log:
            try:
                if log["event"] == "Location":
                    station_name = log.get("StationName", "")
                    print(f"Found station: {station_name}")
                    return station_name
            except Exception: # If it gets muddled, it will return "Unknown station"
                print("No station found")
                return "Unknown station" 


def eventHandler(event, logLineNum):
    """
    Event handler for journal events. 
    Run once per line.
    Accepts event as string.
    If the event is not recognized, it will return 1.
    If the event is recognized, it will return the event type as a string.
    If it detects a shutdown, it will return 0.
    
    """
    print("Parsing log data - looking for events in " + str(event) + "...")
    #Error handling
    if event == "Shutdown":
        return 0
    if event == "Fileheader":
        return 1
    if event == "Location":
        print("Found event: Location. Checking if docked")
        if load(journalPath)[logLineNum]["Docked"] == True:
            print("Docked")
            return "Docked at " + getStation(load(journalPath))
        else:
            print("Not docked")
            return "Flying in " + getSystem(load(journalPath))

    if event in eventAssociationsMain:
        if eventAssociationsMain[event] == "Fileheader":
            print("Fileheader found, skipping")
        else:
            print(f"Found event: {event}")
            system = getSystem(load(journalPath))
            return eventAssociationsMain[event] + system
    elif event in eventAssociationsDocked:
        station = getStation(load(journalPath))
        if station:  # Check if the string exists
            print(f"Returning: {eventAssociationsDocked[event] + station}")
            return eventAssociationsDocked[event] + station
        else:
            return eventAssociationsDocked[event] + "a station"
    else:
        print(f"Unknown event: {event}")
        return 1
