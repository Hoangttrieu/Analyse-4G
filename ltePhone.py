from datetime import datetime, timedelta, time
#def readfile(path):
path=r"C:\Users\trieuhoang\Desktop\document\Documentations\RennesBrestVoiture\zk_0000013797_20180404153957_test.txt"
#filename=getfileName(path)
file=open(path,"r")
linestack=[] #list of message
timeVar = []
#fill the messages into list linestack
for line in file:
    words = line.split(",")
    line = words
   # if (line[0] == "ML"):
    if (line[0].find("@END")!=0):
        if  (line[0].find("START")!=0):
            print(line[0])
   # timeArr=datetime.strptime(str(line[3]), '%H:%M:%S.%f')
    #line[3] = (timeArr+ timedelta(microseconds=1)).time()
    #linestack.append(line)
    #message.append(line)
   # timeVar.append(line[3])

    #return Dis_groupName, coordinates, filename
