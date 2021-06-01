from os import remove, listdir, system, chdir
from shutil import rmtree
chdir("C:/system")
try:
    remove('C:/Users/admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup/lancement.pyw')
except:
    pass
for file in listdir():  
    system(f"attrib -h -s -r {file}")
try:
    rmtree("C:/system")
except:
    pass