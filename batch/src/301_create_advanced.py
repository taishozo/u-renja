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

with open("../../static/iiif/collection/advanced.json") as f:
    collection = json.load(f)

manifests = collection["manifests"]

actions = []

for m in manifests:

    fulltext = ""

    item = {
        "objectID" : str(m["label"]),
    }

    metadata = m["metadata"]

    for me in metadata:
        value = me["value"]
        if value != "":
            item[me["label"]] = value
            fulltext += ", " + value
    
    item["fulltext"] = fulltext
    actions.append(item)

f2 = open("../../static/data/advanced.json", 'w')
json.dump(actions, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))