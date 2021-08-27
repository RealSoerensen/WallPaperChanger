import ctypes
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
import os
import getpass
import time
import struct
from win32api import GetSystemMetrics

USER_NAME = getpass.getuser()

path = Path(__file__).parent

## Add the script to startup
def add_to_startup():
    bat_path = "C:\\Users\%s\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" % USER_NAME
    with open(bat_path + '\\' + "WallpaperChanger.bat", "w+") as bat_file:
        bat_file.write("start" + " %s" % path + "\RandomWallpaperChanger.pyw")

## Check if windows is 32 or 64 bit
def is_64bit_windows():
    return struct.calcsize('P') * 8 == 64

## Get wallpaper from wallhaven.cc
def getWallpaper():
    wpData = requests.get(f"https://wallhaven.cc/api/v1/search?resolutions={GetSystemMetrics(0)}x{GetSystemMetrics(1)}&sorting=random")
    wpJson = wpData.json()
    wpJson = wpJson.get("data")
    wpUrl = wpJson[0].get("path")
    response = requests.get(wpUrl)
    img = Image.open(BytesIO(response.content))
    imgpath = str(path) + "\\temp.png"
    img.save(imgpath, "PNG")
    setWallpaper(imgpath)

## Set wallpaper
def setWallpaper(img):
    if is_64bit_windows():
        ctypes.windll.user32.SystemParametersInfoW(20, 0, img, 3)
    else:
        ctypes.windll.user32.SystemParametersInfoA(20, 0, img, 3)
    time.sleep(1)
    os.remove(img)

if __name__ == "__main__":
    add_to_startup()
    getWallpaper()
