import os
def getPathText(name):
   # return "C:\\Users\\Trieu Hoang\\Desktop\\ZKCellTest\\network\\" + name
    return os.path.abspath("..\\outputFiles\\" + name)
def getWireshark(application):
    return "C:\\Program Files\\Wireshark\\"+application
