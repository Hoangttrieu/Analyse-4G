import os
import pandas as pd
import json
from datetime import datetime
from constantPath import*
import shapely.geometry as geometry
from shapely.geometry import point,polygon
from PhoneId import*

import numpy as np
from shapely.ops import cascaded_union,polygonize
from scipy.spatial import Delaunay
from math import sin, cos, sqrt, atan2, radians,floor

class traceFromJson:

    def __init__(self,file,oper):
        self.ltephoneName = os.path.abspath("..\\outputFiles\\" + file + "_" + "LTEphone"+"_"+oper.getOperater()+".txt")
        self.jsonSystemInfoName = os.path.abspath("..\\outputFiles\\"+ file + "_" + "final"+ "_"+oper.getOperater()+".txt")

    def createTactable(self):
        df = pd.DataFrame({"TAC": [], "CellID": [], "PCI": [], "EARFCN": [], "geolocation": [],"mcc":[],"mnc":[]})
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
                    mccdigit1=typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"][
                        "lte-rrc.plmn_IdentityList_tree"]["Item 0"]["lte-rrc.PLMN_IdentityInfo_element"][
                        "lte-rrc.plmn_Identity_element"]["lte-rrc.mcc_tree"]["Item 0"]["lte-rrc.MCC_MNC_Digit"]
                    mccdigit2 = typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"][
                        "lte-rrc.plmn_IdentityList_tree"]["Item 0"]["lte-rrc.PLMN_IdentityInfo_element"][
                        "lte-rrc.plmn_Identity_element"]["lte-rrc.mcc_tree"]["Item 1"]["lte-rrc.MCC_MNC_Digit"]
                    mccdigit3 = typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"][
                        "lte-rrc.plmn_IdentityList_tree"]["Item 0"]["lte-rrc.PLMN_IdentityInfo_element"][
                        "lte-rrc.plmn_Identity_element"]["lte-rrc.mcc_tree"]["Item 2"]["lte-rrc.MCC_MNC_Digit"]
                    mncdigit1=mccdigit1=typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"][
                        "lte-rrc.plmn_IdentityList_tree"]["Item 0"]["lte-rrc.PLMN_IdentityInfo_element"][
                        "lte-rrc.plmn_Identity_element"]["lte-rrc.mnc_tree"]["Item 0"]["lte-rrc.MCC_MNC_Digit"]
                    mncdigit2 = mccdigit1 = typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"][
                        "lte-rrc.plmn_IdentityList_tree"]["Item 0"]["lte-rrc.PLMN_IdentityInfo_element"][
                        "lte-rrc.plmn_Identity_element"]["lte-rrc.mnc_tree"]["Item 1"]["lte-rrc.MCC_MNC_Digit"]
                    mcc=mccdigit1+mccdigit2+mccdigit3
                    mnc=mncdigit1+mncdigit2
                    cellId = typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"]["lte-rrc.cellIdentity"]
                    pci = dissector["frame"]["frame.comment"]["frame.comment.PCI"]
                    earfcn = dissector["frame"]["frame.comment"]["frame.comment.EARFCN"]
                    coord = geometry.Point(float(dissector["frame"]["frame.comment"]["frame.comment.geolocation"]["latitude"]),float(dissector["frame"]["frame.comment"]["frame.comment.geolocation"]["longitude"]))
                    df1 = pd.DataFrame({"TAC": [trackingAreaCode], "CellID": [cellId], "PCI": [pci], "EARFCN": [earfcn],
                                        "geolocation": [coord],"mcc":[mcc],"mnc":[mnc]})
                    df = df.append(df1, ignore_index=True)
                    #TACtable = df.groupby(["TAC", "CellID"],as_index=False)

        #return TACtable
        return  df


    def createPCItable(self):
        df = pd.DataFrame({"PCI": [], "EARFCN": [], "Geolocation": [],"RSRP":[]})
        jsonLTE = open(self.ltephoneName)
        json_ltes = json.load(jsonLTE)
        for mersurement in json_ltes.keys():
            pci = json_ltes[mersurement]["current cell"]["PCI"]
            rsrp=floor(140+float(json_ltes[mersurement]["current cell"]["RSRP"]["Average RSRP"]))+1
            geolocation = geometry.Point(float(json_ltes[mersurement]["current cell"]["Geolocation"]["latitude"]),float(json_ltes[mersurement]["current cell"]["Geolocation"]["longitude"]))
            earfcn = json_ltes[mersurement]["current cell"]["EARFCN"]
            df3 = pd.DataFrame({"PCI": [pci], "EARFCN": [earfcn], "Geolocation": [geolocation],"RSRP":[rsrp]})
            df = df.append(df3, ignore_index=True)
            pciEarfcnTable = df.groupby(["PCI", "EARFCN"],as_index=False)
        return pciEarfcnTable

    def cellInfo(self,Tactable,pciEarfcnTable,oper):
        TACtable=Tactable.groupby(["TAC", "CellID"],as_index=False)
        df = pd.DataFrame({"cellID": [], "PCI": [], "EARFCN": [], "Geolocation": [],"RSRP":[]})
        for tacTable in TACtable.groups.keys():

            for group, name in TACtable.get_group((tacTable)).groupby(["PCI", "EARFCN"]):
                pci,earfcn=group
                rowNum,colsNum=(TACtable.get_group((tacTable)).groupby(["PCI", "EARFCN"])).get_group((group)).shape
                pointc=geometry.Point(0,0)
                if rowNum>1:
                    for i in range(1,rowNum):
                        pointA =(TACtable.get_group((tacTable)).groupby(["PCI", "EARFCN"])).get_group((group)).iloc[i-1]["geolocation"]
                        pointc=pointA
                        pointB = (TACtable.get_group((tacTable)).groupby(["PCI", "EARFCN"])).get_group((group)).iloc[i]["geolocation"]

                        if pointA.distance(pointB)>0:
                            df4 = pd.DataFrame(
                                {"cellID": [tacTable], "PCI": [pci], "EARFCN": [earfcn], "Geolocation": [pointA],"RSRP":[-1]})
                            df = df.append(df4, ignore_index=True)
                if ((pci,earfcn)) in pciEarfcnTable.groups.keys():
                    (rownum, colsnum) = (pciEarfcnTable.get_group((pci,earfcn))).shape
                    for i in range(0,rownum):
                        #pointC=(TACtable.get_group((tacTable)).groupby(["PCI", "EARFCN"])).get_group((group)).iloc[i - 1]["geolocation"]
                        pointD = pciEarfcnTable.get_group((pci, earfcn)).iloc[i]["Geolocation"]
                        rsrp= pciEarfcnTable.get_group((pci, earfcn)).iloc[i]["RSRP"]
                        if (pointc.distance(pointD)<14):
                            df4 = pd.DataFrame({"cellID": [tacTable], "PCI": [pci], "EARFCN": [earfcn], "Geolocation": [pointD],"RSRP":[float(rsrp)]})
                            df = df.append(df4, ignore_index=True)
        cellList=[]
        Points=[]
        for group, name in df.groupby(["cellID", "PCI"]):
            gr=df.groupby(["cellID", "PCI"]).get_group(group)
            ((tac, cellid),pci) = group
            cell = {"property": str((tac, cellid, pci, list(gr.iloc[[0]]["EARFCN"])[0])),
                    "features": []}
            points=[]
            pointvar=[]
            for index,row in gr.iterrows():
                #cell["features"].append({"lat":str(row["Geolocation"].x), "lon": str(row["Geolocation"].y)})
                points.append({"geo":row["Geolocation"],"rsrp":row["RSRP"]})
                pointvar.append(row["Geolocation"])
            #cellList.append(cell)

            #----------------------------

            convex=geometry.MultiPoint(list(pointvar)).convex_hull
            for point in points:
                if point["geo"].within(convex)==True:
                    cell["features"].append({"lat": str(point["geo"].x), "lon": str(point["geo"].y),"prop":"inside","RSRP":point["rsrp"]})
                else:
                    cell["features"].append({"lat": str(point["geo"].x), "lon": str(point["geo"].y), "prop": "border","RSRP":point["rsrp"]})
            cellList.append(cell)

            #-----------------------------

        with open(getLeaflet("CellInformation""_"+oper.getOperater()+".json"), 'w') as outfile:
            json.dump(cellList, outfile, indent=4, separators=(',', ': '), sort_keys=False)
