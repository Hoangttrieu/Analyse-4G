import os
import ntpath
def getPathText(name):
   # return "C:\\Users\\Trieu Hoang\\Desktop\\ZKCellTest\\network\\" + name
    return os.path.abspath("..\\outputFiles\\" + name)
def getLeaflet(name):
    return os.path.abspath("..\\..\\leaflet\\" + name)
def getWireshark(application):
    return "C:\\Program Files\\Wireshark\\"+application

def getfileName(path):
    return ntpath.split(os.path.splitext(path)[0])[1]

def readfile(pathfile):
    files=[]
    for file in pathfile:
        filename = getfileName(file)
        file = open(file, "r")
        files.append(file)
    return files,filename
