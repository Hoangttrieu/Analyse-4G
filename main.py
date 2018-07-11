from readfile import readfile
from jsonFiles import *
from callWireshark import *
def __main__(pathfile):
    groupname,coordinates=readfile(pathfile)
    pathjson=callWireshark(groupname)
    processingJson(pathjson,coordinates)
__main__("C:\\Users\\Trieu Hoang\\Desktop\\ZKCellTest\\rennes_Brest.txt")
