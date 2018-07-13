import json
from constantPath import *
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
"""
path="C:\\Users\\Trieu Hoang\\Desktop\\ZKCellTest\\network\\dataTraces.txt"
json_data=open(path)
json_objects=json.load(json_data)
frame_object=json_objects[0]["_source"]["layers"]["frame"]
frame_object["frame.abc"]={"frame.abc.geo":{}}
frame_obj=json_objects[0]["_source"]["layers"]["frame"]["frame.abc"]["frame.abc.geo"]={"latitude":"1234","longitude":"456"}
pprint(frame_object)
"""