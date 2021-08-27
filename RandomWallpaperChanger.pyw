import ctypes
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
import os
import getpass
import time

USER_NAME = getpass.getuser()

path = Path(__file__).parent

def add_to_startup():
    bat_path = "C:\\Users\%s\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" % USER_NAME
    with open(bat_path + '\\' + "WallpaperChanger.bat", "w+") as bat_file:
        bat_file.write("start" + " %s" % path + "\RandomWallpaperChanger.pyw")

def getWallpaper():
    wpData = requests.get("https://wallhaven.cc/api/v1/search?resolutions=1920x1080&sorting=random")
    wpJson = wpData.json()
    wpJson = wpJson.get("data")
    wpUrl = wpJson[0].get("path")
    response = requests.get(wpUrl)
    img = Image.open(BytesIO(response.content))
    imgpath = str(path) + "\\temp.png"
    img.save(imgpath, "PNG")
    setWallpaper(imgpath)

def setWallpaper(img):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, img , 0)
    time.sleep(1)
    os.remove(img)

if __name__ == "__main__":
    add_to_startup()
    getWallpaper()
