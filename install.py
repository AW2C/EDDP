import getpass
from time import sleep
import os
USER_NAME = getpass.getuser()


def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:/Users/%s\AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup' % USER_NAME
    with open(bat_path + '/' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)


fp = input("Where is main.py? To find the path, right click on main.py and click 'Copy As Path'")
add_to_startup(file_path=fp)
print("Done!")
sleep(2)