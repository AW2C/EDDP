import json
import os
import glob
import getpass
from log import log

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
    log("Parsing log file", "load")
    log_files = glob.glob(os.path.join(logDir, "*.log"))
    latest_file = max(log_files, key=os.path.getmtime)
    log("Opening log file " + str(latest_file), "load")
    res = []
    with open(latest_file) as f:
        for line in f:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Skip empty lines
                try:
                    data = json.loads(line)
                    res.append(data)
                except json.JSONDecodeError:
                    log(f"Skipping line: {line}", "load")
    res.reverse()  # so that it will stop when at the latest event it recognizes
    return res


def getCMDR(logs):
    """
    Returns the commander name as a string.
    Accepts logs as a list. (array)
    """
    log("Parsing log data", "getCMDR")
    logs.reverse()  # becuase we want the first one. Undoes line 34
    cmdr_name = " "
    for logLine in logs:
        if "event" in logLine:
            try:
                if logLine["event"] == "Commander":
                    cmdr_name = logLine.get("Name", "")
                    log(f"Found commander: {cmdr_name}", "getCMDR")
                    return cmdr_name
            except Exception:
                log("No commander found", "getCMDR")
                return "Unknown"


def getSystem(logs):
    """
    Returns the system name as a string.
    Accepts logs as a list. (array)
    """
    log("Parsing log data - looking for system name", "getSystem")
    system_name = " "
    for logLine in logs:
        if "event" in logLine:
            try:
                if logLine["event"] == "Location":
                    system_name = logLine.get("StarSystem", "")
                    log(f"Found system: {system_name}", "getSystem")
                    return system_name  # because we start with the latest one, we can just return it straight away
                if logLine["event"] == "FSDJump":
                    system_name = logLine.get("StarSystem", "")
                    log(f"Found system: {system_name}", "getSystem")
                    return system_name
            except Exception:
                log("No system found", "getSystem")
                return "Unknown system"


def getStation(logs):
    """
    Returns the station name as a string.
    Accepts logs as a list. (array)
    """
    log("Parsing log data - looking for station", "getStation")
    for logLine in logs:
        if "event" in logLine:
            try:
                if logLine["event"] == "Location":
                    station_name = logLine.get("StationName", "")
                    log(f"Found station: {station_name}", "getStation")
                    return station_name
            except Exception:  # If it gets muddled, it will return "Unknown station"
                log("No station found", "getStation")
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
    log(f"Parsing log data - looking for events in {event}...", "eventHandler")

    # Error handling
    if event == "Shutdown":
        return 0
    if event == "Fileheader":
        return 1

    # Check if docked
    if event == "Location":
        log("Found event: Location. Checking if docked", "eventHandler")
        is_docked = load(journalPath)[logLineNum]["Docked"]
        if is_docked:
            log("Docked")
            return f"Docked at {getStation(load(journalPath))}"
        else:
            log("Not docked")
            return f"Flying in {getSystem(load(journalPath))}"

    # Check event associations
    event_associations = eventAssociationsMain if event in eventAssociationsMain else eventAssociationsDocked
    if event in event_associations:
        log(f"Found event: {event}", "eventHandler")
        location = getStation(load(journalPath)) if event in eventAssociationsDocked else getSystem(load(journalPath))
        return f"{event_associations[event]}{location}"
    else:
        log(f"Unknown event: {event}", "eventHandler")
        return 1
