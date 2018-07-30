from readfile import readfile
from jsonFiles import *
from callWireshark import *
def __main__(pathfile):
    groupname,coordinates,filename,pci,earfcn=readfile(pathfile)
    pathjson=callWireshark(groupname,filename)
    processingJson(pathjson,coordinates,filename,pci,earfcn)

__main__(r"C:\Users\Trieu Hoang\Desktop\ZKCellTest\RennesBrestVoiture\zk_0000013797_20180404120733_test.txt")
