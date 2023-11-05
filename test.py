
import pystray
from PIL import Image
 
image = Image.open("D:\github\EDDP\EDDP\icon.png")
 
 
def after_click(icon, query):
    if str(query) == "Exit":
        icon.stop()
 
 
icon = pystray.Icon("GFG", image, "GeeksforGeeks", 
                    menu=pystray.Menu(
    pystray.MenuItem("Exit", after_click)))
 
icon.run()
print("test")