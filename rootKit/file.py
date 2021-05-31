import subprocess, os, requests
class File():
    def __init__(self, path):
        self.path = path
        os.chdir(path)
    def hide(self, filename, dir=None):
        if dir:
            dir = f"cd {dir}/"
        if type(filename) == list:
            for file in filename:
                subprocess.Popen(f"attrib +h +s +r {file}", shell=True)
            return True
        subprocess.Popen(f"attrib +h +s +r {filename}", shell=True)
        return True
    def unhide(self, filename, dir=None):
        if dir:
            dir = f"cd {dir}/"
        if type(filename) == list:
            for file in filename:
                subprocess.Popen(f"attrib -h -s -r {file}", shell=True)
            return True
        subprocess.Popen(f"attrib -h -s -r {filename}", shell=True)
        return True
    def change(self, dir):
        self.path = dir
        os.chdir(dir)
    def getPath(self):
        return self.path
    def modify(self, filename, url):
        with open(filename, 'w'):
            pass
        with open(filename, "a") as file:
            for line in requests.get(f"{url}").text.split('\n'):
                file.write(line)
    def Read(self, filename, lines=False, words=False, letters=False):
        with open(filename, "r") as file:
            if lines or words or letters:
                ret = []
                if letters:
                    LINE = []
                    WORD = []
                    LETTERS = []
                    for line in file.readlines():
                        line = line.replace('\n', "")
                        LINE.append(line.replace("\n", ""))
                        for word in line.split():
                            WORD.append(word)
                            LETTERS.append(list(word))
                    ret.append(LINE)
                    ret.append(WORD)
                    ret.append(LETTERS)
                    return ret
                if words:
                    LINE = []
                    WORD = []
                    for line in file.readlines():
                        line = line.replace('\n', "")
                        LINE.append(line.replace("\n", ""))
                        for word in line.split():
                            WORD.append(word)
                    ret.append(LINE)
                    ret.append(WORD)
                    return ret
                if lines:
                    app = []
                    for line in file.readlines():
                        app.append(line.replace("\n", ""))
                    ret.append(app)
                    return ret
            return file.read()
    def getByGithub(self, url):
        return requests.get(f"{url}").text