import os
import json
import pandas as pd
from constantPath import *
import webbrowser
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime
from pprint import pprint
import shapely.geometry as geometry
import math
import numpy as np
from shapely.ops import cascaded_union,polygonize
path=os.path.abspath("..\\outputFiles\\zk_0000013797_20180404120733_test_final.txt")
pathlte=os.path.abspath("..\\outputFiles\\zk_0000013797_20180404120733_test_LTEphone.txt")

def getJsonfile(path):
    df= pd.DataFrame({"TAC":[],"CellID":[],"PCI":[],"EARFCN":[],"geolocation":[]})
    jsonObject= open(path)
    json_objects=json.load(jsonObject)
    for jsonfile in json_objects:
        dissector=jsonfile["_source"]["layers"]
        if "lte-rrc.BCCH_DL_SCH_Message_element" in (dissector).keys():
            typemess=dissector["lte-rrc.BCCH_DL_SCH_Message_element"]["lte-rrc.message_tree"]["lte-rrc.c1_tree"]
            sib1 = list((typemess).keys())[0]
            if sib1 == "lte-rrc.systemInformationBlockType1_element":
                trackingAreaCode = typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"]["lte-rrc.trackingAreaCode"]
                cellId=typemess[sib1]["lte-rrc.cellAccessRelatedInfo_element"]["lte-rrc.cellIdentity"]
                pci= dissector["frame"]["frame.comment"]["frame.comment.PCI"]
                earfcn = dissector["frame"]["frame.comment"]["frame.comment.EARFCN"]
                coord=dissector["frame"]["frame.comment"]["frame.comment.geolocation"]
                df1=pd.DataFrame({"TAC":[trackingAreaCode],"CellID":[cellId],"PCI":[pci],"EARFCN":[earfcn],"geolocation":[coord]})
                df=df.append(df1,ignore_index=True)
                TACtable=df.groupby(["TAC","CellID"])
    return TACtable

def distance(pointA,pointB):
    R=6373.0
    lat1 = radians(float(pointA["latitude"]))
    lon1 = radians(float(pointA["longitude"]))
    lat2 = radians(float(pointB["latitude"]))
    lon2 = radians(float(pointB["longitude"]))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def getMesurementFile(pathLTE):
    df=pd.DataFrame({"PCI":[],"EARFCN":[],"Geolocation":[]})
    jsonLTE=open(pathLTE)
    json_ltes=json.load(jsonLTE)
    for mersurement in json_ltes.keys():
        timeJson=datetime.strptime(json_ltes[mersurement]["current cell"]["Time"], '%Y-%m-%d %H:%M:%S.%f')
        pci = json_ltes[mersurement]["current cell"]["PCI"]
        geolocation=json_ltes[mersurement]["current cell"]["Geolocation"]
        earfcn=json_ltes[mersurement]["current cell"]["EARFCN"]
        df3 = pd.DataFrame({ "PCI": [pci],"EARFCN":[earfcn], "Geolocation": [geolocation]})
        df=df.append(df3,ignore_index=True)
    #df=(df.sort_values("Time")).reset_index(drop=True)
    pciEarfcnTable=df.groupby(["PCI","EARFCN"])
    return pciEarfcnTable

TACtable = getJsonfile(path)
pciEarfcnTable= getMesurementFile(pathlte)
#print(pciEarfcnTable.groups.keys())
#print(TACtable.last())
#print(TACtable.get_group(('0d:ac', '64:3c:a5:10')).groupby(["PCI","EARFCN"]).last())
df=pd.DataFrame({"cellID":[],"PCI":[],"EARFCN":[],"Geolocation":[]})

for tacTable in TACtable.groups.keys():
    (tac,cell)=tacTable
    geoloc=[]
    pciGroupbytable=TACtable.get_group((tacTable)).groupby(["PCI","EARFCN"])
    cellPCI=list(pciGroupbytable.groups.keys())[0]
    (pci,earfcn)=cellPCI
    pciGroupbytable.get_group((cellPCI))
    for coordi in pciGroupbytable.get_group((cellPCI))["geolocation"].tolist():
        if coordi not in geoloc:
            geoloc.append(coordi)
    if cellPCI in pciEarfcnTable.groups.keys():
        buffgeo=[]
        for i in range (len(geoloc)):
            geolocLTE = pciEarfcnTable.get_group((cellPCI))["Geolocation"].tolist()
            for j in range(len(geolocLTE)):
                dis=distance(geoloc[i],geolocLTE[j])
                if (dis>0 and dis < 14):
                    if geolocLTE[j] not in buffgeo:
                        buffgeo.append(geolocLTE[j])
        geoloc=geoloc+buffgeo
    df4=pd.DataFrame({"cellID":[tacTable],"PCI":[pci],"EARFCN":[earfcn],"Geolocation":[geoloc]})
    df=df.append(df4,ignore_index=True)
# write file for leaflet
cellList=[]
test=[]

#listpoints=[]
for group, name in df.groupby(["cellID","PCI"]):
    gr=df.groupby(["cellID","PCI"]).get_group(group)

    (tac,cellid)=list(gr["cellID"])[0]
    cell={"property":str((tac,cellid,list(gr["PCI"])[0],list(gr["EARFCN"])[0])),
    "features":[]}
    listGeo=list((df.groupby(["cellID","PCI"])).get_group(group)["Geolocation"])[0]
    test.append(listGeo)
    points=[]
    #lat=[float(geolocation["latitude"]) for geolocation in listGeo]
    #lon = [float(geolocation["longitude"]) for geolocation in listGeo]
    #points=geometry.Point(lat,lon)
    #x, y = concave.exterior.coords.xy
    for geolocation in listGeo:
        latitude = geolocation["latitude"]
        longitude = geolocation["longitude"]
        cell["features"].append({"lat":latitude,"lon":longitude})
        points.append(geometry.Point(float(latitude),float(longitude)))
    cellList.append(cell)
   # concave = concave_hull(points)
   # x, y = concave.exterior.coords.xy
    #listpoints.append(points)

#print(count)
with open(getLeaflet("CellInformation.json"), 'w') as outfile:
   json.dump(cellList, outfile, indent=4, separators=(',', ': '), sort_keys=False)
#firefox=webbrowser.get('firefox')
#print (webbrowser._browsers)
#-------------
import pylab as pl
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from descartes import PolygonPatch
#x = [p.coords.xy[0] for p in listpoints[6]]
#y = [p.coords.xy[1] for p in listpoints[6]]

def plot_polygon(polygon):
    fig = pl.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    x_min, y_min, x_max, y_max = polygon.bounds
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    patch = PolygonPatch(polygon, fc='#999999',
                         ec='#000000', fill=True,
                         zorder=-1)
    ax.add_patch(patch)
    return fig
def concave_hull(points):
    alpha=1
    if len(points)<4:
        return geometry.MultiPoint(list(points)).convex_hull

    def add_edge(edges, edge_points, coords, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add((i, j))
        edge_points.append(coords[[i, j]])


    coords = np.array([point.coords[0]
                   for point in points])
    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
        # Lengths of sides of triangle
        a = math.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
        b = math.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
        c = math.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
        # Semiperimeter of triangle
        s = (a + b + c) / 2.0
        # Area of triangle by Heron's formula
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)
        # Here's the radius filter.
        # print circum_r
        if circum_r < 1.0 / alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles)
#concave=concave_hull(listpoints[6])
#x,y=concave.exterior.coords.xy
#print(len(x))
#print(len(y))
#print(len(listpoints[6]))
#poin_collection=geometry.MultiPoint(list(listpoints[6]))
#plot_polygon(concave)
#pl.plot(x,y,'o', color='#f16824')
#pl.show()

