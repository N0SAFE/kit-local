import subprocess, math
class Sound():
    def byPercent(self, number):
        if number >= 0:
            return math.floor(number*65535/100)
        return None
    def increase(self, number, unmute = False):
        if unmute:
            Sound.unmute()
        if number:
            subprocess.Popen(f'nircmd.exe changesysvolume {number}', shell=True)
    def decrease(self, number):
        if number:
            subprocess.Popen(f'nircmd.exe changesysvolume -{number}', shell=True)
    def mute(self):
        subprocess.Popen(f'nircmd.exe mutesysvolume 1', shell=True)
    def unmute(self):
        subprocess.Popen(f'nircmd.exe mutesysvolume 0', shell=True)
    def setVolume(self, number, unmute = False):
        if unmute:
            Sound.unmute()
        if number or number == 0:
            if number <= 65535:
                subprocess.Popen(f'nircmd.exe setsysvolume {number}', shell=True)
                return True
            else:
                return False