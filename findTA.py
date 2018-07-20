import os
import json
from pprint import pprint
import pandas as pd
from datetime import datetime
path=os.path.abspath("..\\outputFiles\\zk_0000013797_20180404120733_test_final.txt")
pathlte=os.path.abspath("..\\outputFiles\\zk_0000013797_20180404120733_test_LTEphone.txt")
"""jsonLTE=open(pathlte)
json_ltes=json.load(jsonLTE)
json_data=open(path)
json_objects=json.load(json_data)
SystemInforBlock1=[]
TrackingArea=dict()
for jsonfile in json_objects:
    dissector=jsonfile["_source"]["layers"]
    if "lte-rrc.BCCH_DL_SCH_Message_element" in (dissector).keys():
        typemess =dissector["lte-rrc.BCCH_DL_SCH_Message_element"]["lte-rrc.message_tree"]["lte-rrc.c1_tree"]
        #print(typemess)
        sib1 = list((typemess).keys())[0]
        if sib1=="lte-rrc.systemInformationBlockType1_element":
            coordinate=dissector["frame"]["frame.comment"]["frame.comment.geolocation"]
            cellID=typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"]["lte-rrc.cellIdentity"]
            trackingAreaCode = typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"]["lte-rrc.trackingAreaCode"]
            if trackingAreaCode not in TrackingArea.keys():
                TrackingArea[str(trackingAreaCode)]={}
                TrackingArea[str(trackingAreaCode)][str(cellID)] = []
                (TrackingArea[str(trackingAreaCode)][str(cellID)]).append(coordinate)
            if (trackingAreaCode in TrackingArea.keys() and cellID not in TrackingArea[str(trackingAreaCode)]):
                TrackingArea[str(trackingAreaCode)][str(cellID)] = []
                (TrackingArea[str(trackingAreaCode)][str(cellID)]).append(coordinate)
for mersurement in json_ltes.keys():
    cellid = json_ltes[mersurement]["current cell"]["PCI"]
    #print(TrackingArea.keys())
    for cell in TrackingArea.keys():
        print(cellid)
        print(cell)
        if cellid == cell:
            print (cellid)
            trackingAreaCode[cell][cellid].append(json["current cell"]["Geolocation"])
pprint(TrackingArea)"""
#df=pd.DataFrame({"Time":[],"TAC":[],"CID":[],"PCI":[],"Geolocation":[]})
df=pd.DataFrame({"PCI":[],"EARFCN":[],"Geolocation":[]})
"""
json_data=open(path)
json_objects=json.load(json_data)

for jsonfile in json_objects:
    dissector=jsonfile["_source"]["layers"]
    if "lte-rrc.BCCH_DL_SCH_Message_element" in (dissector).keys():
        typemess =dissector["lte-rrc.BCCH_DL_SCH_Message_element"]["lte-rrc.message_tree"]["lte-rrc.c1_tree"]
        sib1 = list((typemess).keys())[0]

        if sib1=="lte-rrc.systemInformationBlockType1_element":
            coordinate=dissector["frame"]["frame.comment"]["frame.comment.geolocation"]
            pci=dissector["frame"]["frame.comment"]["frame.comment.geolocation"]
            time = dissector["frame"]["frame.time"].split()[0:4]
            datetime_object = datetime.strptime(time[2] + " " + time[0] + " " + time[1] + " " + time[3],
                                                '%Y %b %d, %H:%M:%S.%f000')
            cellID = typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"]["lte-rrc.cellIdentity"]
            trackingAreaCode = typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"]["lte-rrc.trackingAreaCode"]
            #df1=pd.DataFrame({"Time":[datetime_object],"TAC":[trackingAreaCode],"CID":[cellID],"PCI":[""],"Geolocation":[""]})
            #df=df.append(df1,ignore_index=True)
"""
jsonLTE=open(pathlte)
json_ltes=json.load(jsonLTE)
for mersurement in json_ltes.keys():
    timeJson=datetime.strptime(json_ltes[mersurement]["current cell"]["Time"], '%Y-%m-%d %H:%M:%S.%f')
    pci = json_ltes[mersurement]["current cell"]["PCI"]
    geolocation=(json_ltes[mersurement]["current cell"]["Geolocation"]["Latitude"],json_ltes[mersurement]["current cell"]["Geolocation"]["Longitude"])
    earfcn=json_ltes[mersurement]["current cell"]["EARFCN"]
    df3 = pd.DataFrame({ "PCI": [pci],"EARFCN":[earfcn], "Geolocation": [geolocation]})
    df=df.append(df3,ignore_index=True)
    #df = df.append(df1, ignore_index=True)
#df=(df.sort_values("Time")).reset_index(drop=True)
#for i in range(len(df)):
#    if df["TAC"][i+1]=="":
#    print(df["TAC"][i])
#print(df)
pciEarfcnTable=df.groupby(["PCI","EARFCN","Geolocation"])
pprint(pciEarfcnTable.last())
#print(df.groupby(["TAC","CID","Geolocation"]).size())

