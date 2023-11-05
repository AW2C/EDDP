from discordrp import Presence
import time
import getpass
import os
import pystray
from PIL import Image
import threading

from game import getCMDR, load, getSystem, eventHandler
global username
username = getpass.getuser()

def create_icon():
    # Create an image for the icon
    image = Image.open('D:\github\EDDP\EDDP\icon.png')
    icon = pystray.Icon("EDDP", image)

    # Define the action to be taken when the icon is clicked
    def action(icon, item):
        icon.stop()

    # Add a menu item to the icon
    icon.menu = pystray.Menu(pystray.MenuItem('Quit', action))

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

def mainGameLoop():
    print("Starting game loop")
    start_time = int(time.time())

    with Presence(client_id) as presence:
        logFileLoaded = load("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous")
        print("Connected")
        cmdr = getCMDR(logFileLoaded)
        updatePrecense(presence, "In the main menu", start_time, cmdr)
        print("Presence updated")

        while True:
            time.sleep(15)
            logs = load("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous")
            for log in logs:
                if "event" in log:
                    currently = eventHandler(log["event"])
            if currently == "0":
                print("Shutting down...")
                break
            else:        
                updatePrecense(presence, currently, start_time, cmdr)

if __name__ == "__main__":
    icon_thread = threading.Thread(target=create_icon)

    # Start the thread
    icon_thread.start()
    awaitGame()