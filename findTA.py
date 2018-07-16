import os
import json
from pprint import pprint
path=os.path.abspath("..\\outputFiles\\zk_0000013797_20130101102811_test_final.txt")
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
pprint(TrackingArea)


