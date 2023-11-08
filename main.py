from discordrp import Presence
import time
import getpass
import os
import pystray
from PIL import Image
import threading

from game import getCMDR, load, eventHandler
global username
username = getpass.getuser()
global currently
currently = "nope"
global shutdownBool
shutdownBool = False

#the icon for the tray
def create_icon():
    image = Image.open('D:\github\EDDP\EDDP\icon.png')
    icon = pystray.Icon("EDDP", image)
    #action for exit
    def action(icon, item):
        shutdownBool = True
        icon.stop()
    #action for the status text
    def action_online(icon, item):
        print("Online!")

    # Add a menu item to the icon
    icon.menu = pystray.Menu(
        pystray.MenuItem('Online!', action_online),
        pystray.MenuItem('Quit', action)
        )

    # Run the icon
    icon.run()


def awaitGame():
    print("Awaiting game")
    while True:
        #list logs dir
        listOne = os.listdir("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous")
        time.sleep(15)
        listTwo = os.listdir("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous")
        if listOne != listTwo:
            print("Game found")
            mainGameLoop()
        else:
            print("Game not found")
            pass

def updatePrecense(presence, state, start_time, cmdr):
    state = str(state) + ".."
    presence.set(
        {
            "state": str(state),
            "details": "Playing Elite: Dangerous as CMDR " + str(cmdr),
            "timestamps": {
                "start": start_time,
            },
            "assets": {
                "large_image": "ed_main",  

            },

            
        }
    )

client_id = "1170388114498392095"  

def mainGameLoop():
    currently = "Loading EDDP..."
    print("Starting game loop")
    currently = " "
    start_time = int(time.time())

    with Presence(client_id) as presence:
        logFileLoaded = load("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous")
        print("Connected")
        cmdr = getCMDR(logFileLoaded)
        updatePrecense(presence, "In the main menu", start_time, cmdr)
        print("Presence updated")

        while True:
            if shutdownBool == True:
                print("Shutdown detected, exiting...")
                break
            time.sleep(15)
            logs = load("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous")
            j = 0
            while j < len(logs):
                logLineNow = logs[j]
                now = eventHandler(logLineNow["event"], j)
                print("Event: " + str(now) + " No: " + str(j))
                j += 1
                if now != 1:
                    currently = now
                    break
                else: 
                    pass

            if now == 0:
                print("Exiting...")
                break
            updatePrecense(presence, currently, start_time, cmdr)
            
            
if __name__ == "__main__":
    icon_thread = threading.Thread(target=create_icon)

    # Start the thread
    icon_thread.start()
    mainGameLoop()
    #remember to look at jumping error! and docking granted error :D