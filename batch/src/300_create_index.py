import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import yaml
import requests

with open("../../static/iiif/collection/top.json") as f:
    collection = json.load(f)

with open("../../static/iiif2/collection/top.json") as f:
    collection2 = json.load(f)

map = {}

manifests2 = collection2["manifests"]
for m in manifests2:
    no = ""
    id = m["@id"]

    for obj in m["metadata"]:
        if obj["label"] == "Description":
            no = obj["value"][0].split(" ")[1]

    if no not in map:
        map[no] = []
    map[no].append(id)

manifests = collection["manifests"]

actions = []

for m in manifests:

    fulltext = ""

    item = {
        "objectID" : str(m["label"]).zfill(4),
    }

    metadata = m["metadata"]

    for me in metadata:
        
        label = me["label"]
        value = me["value"]

        if label == "通番":
            value = int(value)
        
        item[label] = value 

        fulltext += ", " + str(value)

    id = item["objectID"]

    if id in map:
        item["relatedLink"] = map[id]
    
    item["fulltext"] = fulltext
    actions.append(item)

f2 = open("../../static/data/index.json", 'w')
json.dump(actions, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))