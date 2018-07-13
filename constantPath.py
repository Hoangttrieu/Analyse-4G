import os
import ntpath
def getPathText(name):
   # return "C:\\Users\\Trieu Hoang\\Desktop\\ZKCellTest\\network\\" + name
    return os.path.abspath("..\\outputFiles\\" + name)
def getWireshark(application):
    return "C:\\Program Files\\Wireshark\\"+application

path="C:\\Users\\Trieu Hoang\\Desktop\\ZKCellTest\\network\\rennes_brest.txt"
def getfileName(path):
    return ntpath.split(os.path.splitext(path)[0])[1]

