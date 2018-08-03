from datetime import datetime, timedelta, time
import subprocess
from constantPath import*
import json
import pandas as pd

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

    def writejsonMessage(self,oper,MLmessages,PLmessages):
        for line in oper.messages:
            messagetype=messageType(line)
            messagetype.getTime(3)
            if (messagetype.messageType == "ML"):
                MLmessages.gettimeVar(messagetype.message)
                MLmessages.getPCIs(messagetype.message)
                MLmessages.getEARFCNs(messagetype.message)
                MLmessages.setMessages(messagetype.message)
            elif (messagetype.messageType == "PL"):
                PLmessages.setMessages(messagetype.message)
        groupname=MLmessages.writejson(MLmessages.stackmessage,MLmessages.timeVar,oper)
        return groupname



