import json
from constantPath import *
def processingJson(pathnamefile,coordinates):
    json_data=open(pathnamefile)
    json_objects=json.load(json_data)
    for i in range (0,len(json_objects)):
        frame_object=json_objects[i]["_source"]["layers"]["frame"]
        frame_object["frame.comment"] = coordinates[i]
    with open(getPathText('dataTraces.txt'), 'w') as outfile:
        json.dump(json_objects, outfile,  indent=4, separators=(',', ': '), sort_keys=False)

