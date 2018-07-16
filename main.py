from readfile import readfile
from jsonFiles import *
from callWireshark import *
def __main__(pathfile):
    groupname,coordinates,filename=readfile(pathfile)
    pathjson=callWireshark(groupname,filename)
    processingJson(pathjson,coordinates,filename)

__main__(r"C:\Users\Trieu Hoang\Desktop\ZKCellTest\RennesBrestenTrain\zk_0000013797_20130101102811_test.txt")
