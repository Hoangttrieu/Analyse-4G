from datetime import datetime, timedelta, time
from constantPath import*
def getCoordinate(message,j,stack):
    coordinate = {"latitude":message[j],"longitude":message[j+1]}
    stack.append(coordinate)
    return stack

def readfile(path):
    filename=getfileName(path)
    file=open(path,"r")
    linestack=[] #list of message
    message=[]
    BCCH_BCH_148=[]
    BCCH_DL_149=[]
    PCCH_DL_150=[]
    CCCH_DL_151=[]
    CCCH_UL_152=[]
    DCCH_DL_153=[]
    DCCH_UL_154=[]
    Dis_group=[BCCH_BCH_148,BCCH_DL_149,PCCH_DL_150,CCCH_DL_151,CCCH_UL_152,DCCH_DL_153,DCCH_UL_154]
    Dis_groupName=["BCCH_BCH_148","BCCH_DL_149","PCCH_DL_150","CCCH_DL_151","CCCH_UL_152","DCCH_DL_153","DCCH_UL_154"]
    timeVar = []
    #fill the messages into list linestack
    for line in file:
        words = line.split(",")
        line = words
        if (line[0] == "ML"):
            timeArr=datetime.strptime(str(line[3]), '%H:%M:%S.%f')
            line[3] = (timeArr+ timedelta(microseconds=1)).time()
            linestack.append(line)
            message.append(line)
            timeVar.append(line[3])
    # find the message MG
    coordinates=[] #latitude,longitude

    for i in range(0,len(linestack)):
        if (i>0):
            time_object = datetime.strptime(str(linestack[i-1][3]), '%H:%M:%S.%f')
            if (timeVar[i]==timeVar[i-1]):
                linestack[i][3] = (time_object + timedelta(microseconds=1)).time()
        getCoordinate(linestack[i],7,coordinates)
        if (linestack[i][33]=="BC" and linestack[i][34]=="BCH" ):
            BCCH_BCH_148.append(linestack[i])
        elif (linestack[i][33]=="BC" and linestack[i][34]=="DL-S"):
            BCCH_DL_149.append(linestack[i])
        elif (linestack[i][33]=="PC" and linestack[i][34]=="DL-S"):
            PCCH_DL_150.append(linestack[i])
        elif (linestack[i][33]=="CC" and linestack[i][34]=="DL-S"):
            CCCH_DL_151.append(linestack[i])
        elif (linestack[i][33]=="CC" and linestack[i][34]=="UL-S"):
            CCCH_UL_152.append(linestack[i])
        elif (linestack[i][33]=="DC" and linestack[i][34]=="DL-S"):
            DCCH_DL_153.append(linestack[i])
        elif (linestack[i][33]=="DC" and linestack[i][34]=="UL-S"):
            DCCH_UL_154.append(linestack[i])
    for j in range (0,len(Dis_group)):
        writeText(Dis_group[j],Dis_groupName[j],40)
    writeText(message,"message", 0)
    return Dis_groupName, coordinates, filename

def writeText(message,name,start_position):
    nameFile = "%s.txt" % str(name)
    path = getPathText(nameFile)
    f = open(path, 'w')
    for mess in message:
        time=mess[2] + " " + str(mess[3])
        f.write(time)
        f.write("\n")
        f.write("0000")
        for j in range (start_position,len(mess)):
            f.write(" ")
            f.write(str(mess[j]))
        f.write("\n")
    f.close()
