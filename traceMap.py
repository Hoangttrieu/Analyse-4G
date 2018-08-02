import os
import pandas as pd
import json
from datetime import datetime
from constantPath import*
import shapely.geometry as geometry
from PhoneId import*
class traceFromJson:

    def __init__(self,file,oper):
        self.ltephoneName = os.path.abspath("..\\outputFiles\\" + file + "_" + "LTEphone"+"_"+oper.getOperater()+".txt")
        self.jsonSystemInfoName = os.path.abspath("..\\outputFiles\\"+ file + "_" + "final"+ "_"+oper.getOperater()+".txt")

    def createTactable(self):
        df = pd.DataFrame({"TAC": [], "CellID": [], "PCI": [], "EARFCN": [], "geolocation": []})
        jsonObject = open(self.jsonSystemInfoName)
        json_objects = json.load(jsonObject)
        for jsonfile in json_objects:
            dissector = jsonfile["_source"]["layers"]
            if "lte-rrc.BCCH_DL_SCH_Message_element" in (dissector).keys():
                typemess = dissector["lte-rrc.BCCH_DL_SCH_Message_element"]["lte-rrc.message_tree"]["lte-rrc.c1_tree"]
                sib1 = list((typemess).keys())[0]
                if sib1 == "lte-rrc.systemInformationBlockType1_element":
                    trackingAreaCode = typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"][
                        "lte-rrc.trackingAreaCode"]
                    cellId = typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"]["lte-rrc.cellIdentity"]
                    pci = dissector["frame"]["frame.comment"]["frame.comment.PCI"]
                    earfcn = dissector["frame"]["frame.comment"]["frame.comment.EARFCN"]
                    coord = geometry.Point(float(dissector["frame"]["frame.comment"]["frame.comment.geolocation"]["latitude"]),float(dissector["frame"]["frame.comment"]["frame.comment.geolocation"]["longitude"]))
                    df1 = pd.DataFrame({"TAC": [trackingAreaCode], "CellID": [cellId], "PCI": [pci], "EARFCN": [earfcn],
                                        "geolocation": [coord]})
                    df = df.append(df1, ignore_index=True)
                    TACtable = df.groupby(["TAC", "CellID"],as_index=False)
        return TACtable

    def createPCItable(self):
        df = pd.DataFrame({"PCI": [], "EARFCN": [], "Geolocation": []})
        jsonLTE = open(self.ltephoneName)
        json_ltes = json.load(jsonLTE)
        for mersurement in json_ltes.keys():
            pci = json_ltes[mersurement]["current cell"]["PCI"]
            geolocation = geometry.Point(float(json_ltes[mersurement]["current cell"]["Geolocation"]["latitude"]),float(json_ltes[mersurement]["current cell"]["Geolocation"]["longitude"]))
            earfcn = json_ltes[mersurement]["current cell"]["EARFCN"]
            df3 = pd.DataFrame({"PCI": [pci], "EARFCN": [earfcn], "Geolocation": [geolocation]})
            df = df.append(df3, ignore_index=True)
            pciEarfcnTable = df.groupby(["PCI", "EARFCN"],as_index=False)
        return pciEarfcnTable

    def cellInfo(self,TACtable,pciEarfcnTable,oper):
        df = pd.DataFrame({"cellID": [], "PCI": [], "EARFCN": [], "Geolocation": []})
        for tacTable in TACtable.groups.keys():
            print(TACtable.get_group((("38:a2", "0d:a3:a0:10"))).reset_index(drop=True).loc[1]["geolocation"])
            for group, name in TACtable.get_group((tacTable)).groupby(["PCI", "EARFCN"]):
                pci,earfcn=group
                rowNum,colsNum=(TACtable.get_group((tacTable)).groupby(["PCI", "EARFCN"])).get_group((group)).shape
                if rowNum>1:
                    for i in range(1,rowNum):
                        pointA =(TACtable.get_group((tacTable)).groupby(["PCI", "EARFCN"])).get_group((group)).iloc[i-1]["geolocation"]
                        pointB = (TACtable.get_group((tacTable)).groupby(["PCI", "EARFCN"])).get_group((group)).iloc[i]["geolocation"]
                        if pointA.distance(pointB)>0.01:
                            df4 = pd.DataFrame(
                                {"cellID": [tacTable], "PCI": [pci], "EARFCN": [earfcn], "Geolocation": [pointA]})
                            df = df.append(df4, ignore_index=True)
                print(pciEarfcnTable.groups.keys())
                print((pci,earfcn))
                if ((pci,earfcn)) in pciEarfcnTable.groups.keys():
                    (rownum, colsnum) = TACtable.get_group((tacTable)).shape
                    for i in range(rownum):
                        pointC = (TACtable.get_group((tacTable)).groupby(["PCI", "EARFCN"])).get_group((group)).iloc[[0]]["geolocation"]
                        pointD = pciEarfcnTable.get_group((pci, earfcn)).iloc[i]["geolocation"]
                        if (pointC.distance(pointD)<14):
                            df4 = pd.DataFrame({"cellID": [tacTable], "PCI": [pci], "EARFCN": [earfcn], "Geolocation": [pointD]})
                            df = df.append(df4, ignore_index=True)
        cellList=[]
        for group, name in df.groupby(["cellID", "PCI"]):
            gr=pd.DataFrame(df.groupby(["cellID", "PCI"],as_index=False))
            ((tac, cellid),pci) = group
            cell = {"property": str((tac, cellid, pci, gr.iloc[[0]]["EARFCN"])),
                    "features": []}
            listGeo = list((df.groupby(["cellID", "PCI"])).get_group(group)["Geolocation"])[0]
            for index,row in gr.iterrows():
                cell["features"].append({"lat":(row["Geolocation"][0]), "lon": str(row["Geolocation"][0])})
                cellList.append(cell)
        with open(getLeaflet("CellInformation""_"+oper.getOperater()+".json"), 'w') as outfile:
            json.dump(cellList, outfile, indent=4, separators=(',', ': '), sort_keys=False)
