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

prefix = "https://nakamura196.github.io/u-renja"
# prefix = "https://sat-iiif.s3.amazonaws.com"
# prefix = "https://d1av1vcgsldque.cloudfront.net"
opath = "../../static/iiif/collection/top.json"
path = "data/酉蓮社本目録20200819.xlsx"


df_item = pd.read_excel(path, sheet_name="書名", header=None, index_col=None)

r_count = len(df_item.index)
c_count = len(df_item.columns)

map = {}

for i in range(0, c_count):
    map[i] = df_item.iloc[0, i]

manifests = []

for j in range(1, r_count):

    print(str(j)+"/"+str(r_count))

    metadata = []

    for i in map:
        label = map[i]
        value = df_item.iloc[j, i]
        if not pd.isnull(value) and value != 0:
            
            
            value = str(value).strip()

            if label == "譯著者1" or label == "譯著者2" or label == "譯著者3" or label == "譯著者4" or label == "譯著者5" or label == "譯著者6":
                label = "譯著者_facet"

            if label == "通番":
                value = str(value).zfill(4)
            
            metadata.append({
                "label": label,
                "value" : value
            })

            if label == "画像フォルダ名(1)":

                image_flg = "画像なし"
                if value != "":
                    image_flg = "IIIF"

                metadata.append({
                    "label": "画像有無",
                    "value" : image_flg
                })

            if "大正藏採録種別" in label:
                metadata.append({
                    "label": "大正藏採録種別",
                    "value" : value
                })
        elif label == "画像フォルダ名(1)":
            metadata.append({
                "label": "画像有無",
                "value" : "画像なし"
            })

    manifest = {
        # "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Manifest",
        "@id": "http://example.org/"+str(df_item.iloc[j, 7]),
        "license": "aaa",
        # "attribution": df_item.iloc[j, attribution_index],
        "label": df_item.iloc[j, 7],
        "metadata": metadata
    }

    manifests.append(manifest)

collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": prefix + "/iiif/top.json",
    "@type": "sc:Collection",
    "attribution": "酉蓮社",
    "manifests" : manifests,
    "label" : "酉蓮社本目録"
}

f2 = open(opath, 'w')
json.dump(collection, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

