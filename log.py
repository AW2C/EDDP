import datetime
import getpass

username = getpass.getuser()
global logDir 
logDir =  "C:/Users/"+username+"/.AW2C/EDDP/logs"
global logFile
logFile = "LOG - " + str(datetime.datetime.now().strftime("%Y-%m-%d")) + ".log"

def onStart():
    print("EDDP started")
    print("Log file: " + logDir + "/" + logFile)
    print("Log directory: " + logDir)
    print("Log file: " + logFile)