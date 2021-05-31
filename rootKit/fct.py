import os, time, subprocess, math
from os import name
def display(data=None, loop=None, content=None):
    if data == "displayJump":
        for i in range(loop):
            print()
def terminal_size(columns=None, lines=None):
    if columns or lines:
        if name == 'posix':
            if columns:
                subprocess.call(['stty', 'cols', str(columns)], shell=True)
            if lines:
                subprocess.call(['stty', 'rows', str(lines)], shell=True)
        else:
            if columns:
                subprocess.call(['mode', 'con:', 'cols={}'.format(columns)], shell=True)
            if lines:
                subprocess.call(['mode', 'con:', 'lines={}'.format(lines)], shell=True)
    return (((("".join("".join(str(os.get_terminal_size()).split("(")[1]).split(")"))).replace("=", "")).replace("columns", "")).replace("lines", "").split(","))
def endingCode(write=None, temp=None):
    for i in range(math.ceil((int(terminal_size()[0])-35)/2)-1):
        esp=" "*(math.ceil((int(terminal_size()[0])-35)/2)-1)
    clear()
    if temp == None:
        temp = 2
    if write != None:
        print(write)
    display(data="displayJump", loop=15)
    print(f'{fg(3)}{attr(1)}{esp}###################################{reset}')
    print(f'{fg(3)}{attr(1)}{esp}###################################{reset}')
    print(f'{fg(3)}{attr(1)}{esp}###########     end     ###########{reset}')
    print(f'{fg(3)}{attr(1)}{esp}###################################{reset}')
    print(f'{fg(3)}{attr(1)}{esp}###################################{reset}')
    display(data="displayJump", loop=2)
    time.sleep(temp)
    exit()
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def tryImport(data):
    os.system("py -m pip install "+data)   
while True:
        try:
            from colored import fg, bg, attr
            break
        except:
            try:
                tryImport("colored")
            except:
                time.sleep(1)
def getpath(change=False):                          return os.getcwd() if change in (False, "not", "\\") else os.getcwd().replace('\\', '/')
def getSelfFileName():                              return os.path.basename(__file__)
reset = attr('reset')