import subprocess
from constantPath import *
def callWireshark(nameFiles):
    DLT_key={"BCCH_BCH_148":"148",
    "BCCH_DL_149":"149",
    "PCCH_DL_150":"150",
    "CCCH_DL_151":"151",
    "CCCH_UL_152":"152",
    "DCCH_DL_153":"153",
    "DCCH_UL_154":"154"}
    root = getPathText("")+"\\"
    disGroup=[]
    for nameFile in nameFiles:
        name= "%s.txt" %str(nameFile)
        pathInfile = root + name
        pathOutfile = root + "%s.pcap" %str(nameFile)
        disGroup.append(pathOutfile)
        subprocess.check_call([getWireshark("text2pcap.exe"),"-l",DLT_key[nameFile],"-t", "%Y-%m-%d %H:%M:%S.", pathInfile,pathOutfile])
    path= root + "Traces.pcap"
    pathjson=root+"Traces.txt"
    subprocess.check_call(
        [getWireshark("mergecap.exe"), "-w",path,disGroup[0],disGroup[1],disGroup[2]
            ,disGroup[3],disGroup[4],disGroup[5],disGroup[6]])
    tsharkCall=[getWireshark("tshark.exe"),"-T","json","-r",path]
    tsharkOpen=(open(pathjson, "wb"))
    subprocess.call(tsharkCall,stdout=tsharkOpen)
    return pathjson