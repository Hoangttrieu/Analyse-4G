import json
from constantPath import *
from readfile import *
import pandas as pd
import os
from pprint import pprint
def processingJson(pathnamefile,coordinates,namefile):
    json_data=open(pathnamefile)
    json_objects=json.load(json_data)
    for i in range (0,len(json_objects)):
        frame_object=json_objects[i]["_source"]["layers"]["frame"]
       # frame_object["frame.comment"] = coordinates[i]
        frame_object["frame.comment"] = {"frame.comment.geolocalisation":coordinates[i]}
    nameFile=namefile+"_"+"final.txt"
    with open(getPathText(nameFile), 'w') as outfile:
        json.dump(json_objects, outfile,  indent=4, separators=(',', ': '), sort_keys=False)

Dis_groupName, coordinates, filename , ltePhone = readfile(r"C:\Users\trieuhoang\Desktop\document\Documentations\RennesBrestVoiture\zk_0000013797_20180404153957_test.txt")
path = os.path.abspath("..\\outputFiles\\zk_0000013797_20180404153957_test_final.txt")
#df = pd.read_json(path,orient=dict)
#def ltePhone(file):
df = pd.DataFrame(ltePhone)
df1=df[df.columns[71:]]
df.drop(df.columns[71:],axis=1,inplace=True)
df.drop(df.columns[52:70],axis=1,inplace=True)
df.drop(df.columns[47:50],axis=1,inplace=True)
df.drop(df.columns[[0,1,4,5,6,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,28,29,30,31,32,33,37,38,42,43]],axis=1,inplace=True)
df.columns = ["Date","Time","Latitude","Longitude","Mode","EARFCN","PCI","Average RSRP","RSRP Antenna 0","RSRP Antenna 1","Average RSRQ","RSRQ Antenna 0","RSRQ Antenna 1","Average RSSI"
             ,"RSSI Antenna 0","RSSI Antenna 1","SINR Antenna 0","SINR Antenna 1","Number of Neighbors"]
json_objects=dict()
json_obj=dict()

for index,row in df.iterrows():
    neighborList = dict()
    if row["Mode"] == "I":
        row["Mode"] = "idle"
    elif row["Mode"] == "C":
        row["Mode"] = "connected"
    #Find the infos of the neighbors cells
    neighborCount=0
    neighborList= {}
    var=index
    for i in range(0,len(df1.columns),20):
        if df1.iloc[var][71+i+4] is not None:
            neighborCount+=1
            neighborList["Neighbor "+str(neighborCount)]={"PCI": df1.iloc[var][71 + i + 4], "RSRP": df1.iloc[var][71 + i + 6],"RSRQ": df1.iloc[var][71 + i + 7], "RSSI": df1.iloc[var][71 + i + 8]}

    #Prepare the json file
    json_obj["current cell"]={}
    json_obj["current cell"]["Date"]=str(row["Date"])
    json_obj["current cell"]["Time"] =str(df.iloc[var]["Time"])
    json_obj["current cell"]["Localisation_GPS"] = {"Latitude":row["Latitude"],"Longitude":row["Longitude"]}
    json_obj["current cell"]["Mode"]=row["Mode"]
    json_obj["current cell"]["PCI"] = row["PCI"]
    json_obj["current cell"]["EARFCN"] = row["EARFCN"]
    json_obj["current cell"]["RSRP"] = {"Average RSRP":row["Average RSRP"],"RSRP Antenna 0":row["RSRP Antenna 0"],"RSRP Antenna 1":row["RSRP Antenna 1"]}
    json_obj["current cell"]["RSRQ"] = {"Average RSRQ": row["Average RSRQ"], "RSRQ Antenna 0": row["RSRQ Antenna 0"],
                        "RSRQ Antenna 1": row["RSRQ Antenna 1"]}
    json_obj["current cell"]["RSSI"] = {"Average RSSI": row["Average RSSI"], "RSSI Antenna 0": row["RSSI Antenna 0"],
                        "RSSI Antenna 1": row["RSSI Antenna 1"]}
    json_obj["current cell"]["SINR"] = {"SINR Antenna 0": row["SINR Antenna 0"],
                        "SINR Antenna 1": row["SINR Antenna 1"]}
    json_obj["Neighbors cells"]={}
    json_obj["Neighbors cells"]["Number of Neighbors"] = row["Number of Neighbors"]
    json_obj["Neighbors cells"]["information"]=neighborList#neighborList["Mesurement.NeighborCell " + str(index)]
    json_objects["Measurement "+str(index)]=json_obj
pprint(json_objects)
#with open(r"C:\Users\trieuhoang\Desktop\document\test.txt", 'w') as outfile:
#    json.dump(json_objects, outfile, indent=4, separators=(',', ': '), sort_keys=False)




#pprint(df.to_json(orient='table'))
"""
path="C:\\Users\\Trieu Hoang\\Desktop\\ZKCellTest\\network\\dataTraces.txt"
json_data=open(path)
json_objects=json.load(json_data)
frame_object=json_objects[0]["_source"]["layers"]["frame"]
frame_object["frame.abc"]={"frame.abc.geo":{}}
frame_obj=json_objects[0]["_source"]["layers"]["frame"]["frame.abc"]["frame.abc.geo"]={"latitude":"1234","longitude":"456"}
pprint(frame_object)
"""