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

prefix = "https://taishozo.github.io/u-renja"
path = "data/酉蓮社本目録20210226.xlsx"

############

with open("../../static/iiif2/collection/top.json") as f:
    df2 = json.load(f)

manifests = df2["manifests"]

images = {}

for m in manifests:
    metadata = m["metadata"]

    num = -1
    title = ""

    for obj in metadata:
        if "通番: " in obj["value"]:
            num = obj["value"].split("通番: ")[1]

            num = str(int(num))

        elif "Title" in obj["label"]:
            title = obj["value"]

    if num not in images:
        images[num] = []

    images[num].append({
        "id": m["@id"],
        "title": title
    })

#############


df_item = pd.read_excel(path, sheet_name="書名", header=None, index_col=None, engine="openpyxl")
df_item2 = pd.read_excel(path, sheet_name="詳細", header=None, index_col=None, engine="openpyxl")

r_count = len(df_item.index)
c_count = len(df_item.columns)

map = {}

for i in range(0, c_count):
    map[i] = df_item.iloc[0, i]

for j in range(1, r_count):

    print(str(j)+"/"+str(r_count))

    id = df_item.iloc[j, 7]

    if pd.isnull(id):
        continue

    num = -1

    for i in map:
        label = map[i]
        value = df_item.iloc[j, i]
        if not pd.isnull(value) and value != 0:

            value = str(value).strip()

            if label == "大正藏經典番號(1)":
                df_item.iloc[j, i] = "[{}](https://taishozo.github.io/db/search/?keyword={})".format(value, value)

            elif label == "通番":
                num = str(value)

            elif "画像フォルダ名" in label:
                title = df_item.iloc[j, i-1]

                print(title)

                if num in images:
                    
                    arr = images[num]

                    print(arr)

                    for a in arr:
                        if title == a["title"]:
                            df_item.iloc[j, i] = "[{}]({})".format(value, a["id"])


writer = pd.ExcelWriter('../../static/metadata/data.xlsx', engine="openpyxl")
df_item.to_excel(writer, sheet_name = '書名', index=False, header=False)
df_item2.to_excel(writer, sheet_name = '詳細', index=False, header=False)

#Excelファイルを保存
writer.save()
#Excelファイルを閉じる
writer.close()

