from readfile import readfile
from jsonFiles import *
from callWireshark import *

from PhoneId import*

def __main__(pathfile):
  #  groupname,coordinates,filename,pci,earfcn=readfile(pathfile)
  #  pathjson=callWireshark(groupname,filename)
  #  processingJson(pathjson,coordinates,filename,pci,earfcn)
  filename = getfileName(pathfile)
  operaters={}
  file = open(pathfile, "r")
  for line in file:
      words = line.split(",")
      line = words
      if (line[0].find("@START") != 0):
          if (line[0].find("@END") != 0):
              if (line[0]!="HB" and line[0]!="CO" and line[0]!="FE" ):
                 phoneid="phone_"+str(line[5])
                 if (phoneid not in operaters.keys()):
                     operaters[phoneid] = operater(line[5])
                     operaters[phoneid].setMessages(line)
                 else:
                     operaters[phoneid].setMessages(line)



  for oper in operaters.keys():
      MLmessages = mlMessageList()
      groupname=operaters[oper].writejsonMessage(operaters[oper],MLmessages)
      MLmessages.callWireshark(groupname,filename,operaters[oper])

__main__(r"C:\Users\trieuhoang\Desktop\document\Documentations\zk_0000013797_20180731144127.txt")

