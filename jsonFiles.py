import json
from constantPath import *
import pandas as pd

def processingJson(pathnamefile,coordinates,namefile,pci):
    json_data=open(pathnamefile)
    json_objects=json.load(json_data)
    for i in range (0,len(json_objects)):
        frame_object=json_objects[i]["_source"]["layers"]["frame"]
       # frame_object["frame.comment"] = coordinates[i]
        frame_object["frame.comment"] = {"frame.comment.geolocation":coordinates[i],"frame.comment.PCI": pci[i]}
       # frame_object["frame.comment"] = {}
    nameFile=namefile+"_"+"final.txt"
    with open(getPathText(nameFile), 'w') as outfile:
        json.dump(json_objects, outfile,  indent=4, separators=(',', ': '), sort_keys=False)


def getLTEphone(file,namefile):
    df = pd.DataFrame(file)
    df1=df[df.columns[71:]]
    df.drop(df.columns[71:],axis=1,inplace=True)
    df.drop(df.columns[52:70],axis=1,inplace=True)
    df.drop(df.columns[47:50],axis=1,inplace=True)
    df.drop(df.columns[[0,1,4,5,6,9,10,11,12,14,15,16,17,18,19,20,21,22,24,25,28,29,30,31,32,33,37,38,42,43]],axis=1,inplace=True)
    df.columns = ["Date","Time","Latitude","Longitude","Altitude","Mode","EARFCN","PCI","Average RSRP","RSRP Antenna 0","RSRP Antenna 1","Average RSRQ","RSRQ Antenna 0","RSRQ Antenna 1","Average RSSI"
                 ,"RSSI Antenna 0","RSSI Antenna 1","SINR Antenna 0","SINR Antenna 1","Number of neighbours"]
    json_objects=dict()
    for index,row in df.iterrows():
        json_obj = dict()
        neighbourList = dict()
        if row["Mode"] == "I":
            row["Mode"] = "idle"
        elif row["Mode"] == "C":
            row["Mode"] = "connected"
        #Find the infos of the neighbours cells
        neighbourCount=0
        neighbourList= {}
        for i in range(0,len(df1.columns),20):
            if df1.iloc[index][71+i+4] is not None:
                neighbourCount+=1
                neighbourList["neighbour "+str(neighbourCount)]={"PCI": df1.iloc[index][71 + i + 4], "RSRP": df1.iloc[index][71 + i + 6],"RSRQ": df1.iloc[index][71 + i + 7], "RSSI": df1.iloc[index][71 + i + 8]}

        #Prepare the json file
        json_obj["current cell"]={}
        #json_obj["current cell"]["Date"]=row["Date"]
        time=str(row["Time"].strftime('%H:%M:%S.%f'))
        json_obj["current cell"]["Time"] =str(row["Date"])+" "+time

        json_obj["current cell"]["Geolocation"] = {"Latitude":row["Latitude"],"Longitude":row["Longitude"],"Altitude":row["Altitude"]}
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
        json_obj["neighbours cells"]={}
        json_obj["neighbours cells"]["Number of neighbours"] = row["Number of neighbours"]
        json_obj["neighbours cells"]["neighbours.information"]=neighbourList

        json_objects["Measurement "+str(index)]=json_obj

    nameFile = namefile + "_" + "LTEphone.txt"

    with open(getPathText(nameFile), 'w') as outfile:
        json.dump(json_objects, outfile, indent=4, separators=(',', ': '), sort_keys=False)





