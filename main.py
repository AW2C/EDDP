from discordrp import Presence
import time

from game import getCMDR, load, getSystem, eventHandler



def updatePrecense(presence, state, start_time, cmdr):
    presence.set(
        {
            "state": state,
            "details": "Playing Elite: Dangerous as CMDR " + cmdr,
            "timestamps": {
                "start": start_time,
            },
            "assets": {
                "large_image": "ed_main",  

            },

            
        }
    )

client_id = "1170388114498392095"  
start_time = int(time.time())

with Presence(client_id) as presence:
    logFileLoaded = load("C:/Users/Nicey/Saved Games/Frontier Developments/Elite Dangerous")
    print("Connected")
    cmdr = getCMDR(logFileLoaded)
    updatePrecense(presence, "In the main menu", start_time, cmdr)
    print("Presence updated")

    while True:
        time.sleep(15)
        logs = load("C:/Users/Nicey/Saved Games/Frontier Developments/Elite Dangerous")
        for log in logs:
            if "event" in log:
                currently = eventHandler(log["event"])        
        updatePrecense(presence, currently, start_time, cmdr)