from datetime import datetime, timedelta, time
import subprocess
from constantPath import*
class operater:
    def __init__(self,phoneid):
        self.phoneid="phone_"+str(phoneid)
        self.typeMessages=[]
        self.messages=[]
    def getOperater(self):
        return self.phoneid

    def setTypemess(self,mess):
        self.typeMessages.append(mess[0])

    def setMessages(self,message):
        self.messages.append(message)

    def getMessages(self):
        return self.messages

    def writejsonMessage(self,oper,MLmessages):
        for line in oper.messages:
            messagetype=messageType(line)
            messagetype.getTime(3)
            if (messagetype.messageType == "ML"):
                MLmessages.gettimeVar(messagetype.message)
                MLmessages.getPCIs(messagetype.message)
                MLmessages.getEARFCNs(messagetype.message)
                MLmessages.setMessages(messagetype.message)
        groupname=MLmessages.writejson(MLmessages.stackmessage,MLmessages.timeVar,oper)
        return groupname
class messageType:
    def __init__(self,message,time=""):
        self.time=time
        self.message=message
        self.messageType=self.message[0]
    def getTime(self,j):
        timeArr = datetime.strptime(str(self.message[j]), '%H:%M:%S.%f')
        self.message[j] = (timeArr + timedelta(microseconds=1)).time()
        self.time=self.message[j]
        return self.time
class mlMessageList:
    def __init__(self):
        self.PCIs=[]
        self.EARFCNs=[]
        self.coordinates=[]
        self.timeVar=[]
        self.stackmessage=[]

    def getCoordinates(self,message):
        coordinate = {"latitude": message[7], "longitude": message[8]}  # ,"Altitude":message[j+6]}
        self.coordinates.append(coordinate)
        return self.coordinates
    def gettimeVar(self,message):
        self.timeVar.append(message[3])
        return self.timeVar
    def getPCIs(self,message):
        self.PCIs.append(message[20])
        return self.PCIs
    def getEARFCNs(self,message):
        self.EARFCNs.append(message[19])
        return self.EARFCNs
    def setMessages(self,message):
        self.stackmessage.append(message)
        return self.stackmessage

    def writejson(self,stackmessage,timeVar,oper):
        BCCH_BCH_148 = []
        BCCH_DL_149 = []
        PCCH_DL_150 = []
        CCCH_DL_151 = []
        CCCH_UL_152 = []
        DCCH_DL_153 = []
        DCCH_UL_154 = []
        Dis_group = [BCCH_BCH_148, BCCH_DL_149, PCCH_DL_150, CCCH_DL_151, CCCH_UL_152, DCCH_DL_153, DCCH_UL_154]
        Dis_groupName = ["BCCH_BCH_148"+ "_"+oper.getOperater(), "BCCH_DL_149"+ "_"+oper.getOperater(), "PCCH_DL_150"+ "_"+oper.getOperater(),
                         "CCCH_DL_151"+ "_"+oper.getOperater(), "CCCH_UL_152"+ "_"+oper.getOperater(), "DCCH_DL_153"+ "_"+oper.getOperater(),"DCCH_UL_154"+ "_"+oper.getOperater()]
        for i in range(0, len(stackmessage)):
            if (i > 0):
                time_object = datetime.strptime(str(stackmessage[i - 1][3]), '%H:%M:%S.%f')
                if (timeVar[i] == timeVar[i - 1]):
                    stackmessage[i][3] = (time_object + timedelta(microseconds=1)).time()
            self.getCoordinates(stackmessage[i])
            if (stackmessage[i][33] == "BC" and stackmessage[i][34] == "BCH"):
                BCCH_BCH_148.append(stackmessage[i])
            elif (stackmessage[i][33] == "BC" and stackmessage[i][34] == "DL-S"):
                BCCH_DL_149.append(stackmessage[i])
            elif (stackmessage[i][33] == "PC" and stackmessage[i][34] == "DL-S"):
                PCCH_DL_150.append(stackmessage[i])
            elif (stackmessage[i][33] == "CC" and stackmessage[i][34] == "DL-S"):
                CCCH_DL_151.append(stackmessage[i])
            elif (stackmessage[i][33] == "CC" and stackmessage[i][34] == "UL-S"):
                CCCH_UL_152.append(stackmessage[i])
            elif (stackmessage[i][33] == "DC" and stackmessage[i][34] == "DL-S"):
                DCCH_DL_153.append(stackmessage[i])
            elif (stackmessage[i][33] == "DC" and stackmessage[i][34] == "UL-S"):
                DCCH_UL_154.append(stackmessage[i])
        for j in range(0, len(Dis_group)):
            #self.writeText(Dis_group[j],oper,Dis_groupName[j], 40)
            self.writeText(Dis_group[j],Dis_groupName[j], 5)
        return Dis_groupName

    def callWireshark(self,nameFiles, filename,oper):
        DLT_key = {"BCCH_BCH_148"+ "_"+oper.getOperater(): "148",
                   "BCCH_DL_149"+ "_"+oper.getOperater(): "149",
                   "PCCH_DL_150"+ "_"+oper.getOperater(): "150",
                   "CCCH_DL_151"+ "_"+oper.getOperater(): "151",
                   "CCCH_UL_152"+ "_"+oper.getOperater(): "152",
                   "DCCH_DL_153"+ "_"+oper.getOperater(): "153",
                   "DCCH_UL_154"+ "_"+oper.getOperater(): "154"}
        root = getPathText("") + "\\"
        disGroup = []
        for nameFile in nameFiles:
            name = "%s.txt" % str(nameFile)
            pathInfile = root + name
            pathOutfile = root + "%s.pcap" % str(nameFile)
            disGroup.append(pathOutfile)
            subprocess.check_call(
                [getWireshark("text2pcap.exe"), "-l", DLT_key[nameFile], "-t", "%Y-%m-%d %H:%M:%S.", pathInfile,
                 pathOutfile])
        path = root + filename + "_" +"_"+oper.getOperater()+ "final.pcap"  # "Traces.pcap"
        pathjson = root + filename + "_"+oper.getOperater()+"_" + "json.txt"
        subprocess.check_call(
            [getWireshark("mergecap.exe"), "-w", path, disGroup[0], disGroup[1], disGroup[2]
                , disGroup[3], disGroup[4], disGroup[5], disGroup[6]])
        tsharkCall = [getWireshark("tshark.exe"), "-T", "json", "-r", path]
        tsharkOpen = (open(pathjson, "wb"))
        subprocess.call(tsharkCall, stdout=tsharkOpen)
        return pathjson

    def writeText(self,message_list, name, start_position):
       # nameFile = "%s.txt" % str(name+oper.getOperater())
        path = getPathText(str(name)+".txt")
        f = open(path, 'w')
        for mess in message_list:
            time = mess[2] + " " + str(mess[3])
            # time = "2013-03-27" + " " + str(mess[3])
            f.write(time)
            f.write("\n")
            f.write("0000")
            for j in range(start_position, len(mess)):
                f.write(" ")
                f.write(str(mess[j]))
            f.write("\n")
        f.close()


class plMessage(messageType):
    def __init__(self,coordinate,time,message):
        messageType.__init__(self,coordinate,time,message)



