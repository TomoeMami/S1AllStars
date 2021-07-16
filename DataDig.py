# -*- coding: utf-8 -*-
import json
import os

def Merge():
    dirpath = './data'
    rawdata = []
    with open('RawData.json', "w", encoding="utf-8") as f0:
        for file in os.listdir(dirpath):
            with open(os.path.join(dirpath, file), "r", encoding="utf-8") as f1:
                thdata = json.load(f1)
                rawdata = rawdata + thdata
                f1.close()
        f0.write(json.dumps(rawdata,indent=2,ensure_ascii=False))
if __name__ == "__main__":
    # Merge()
    with open('RawData.json', "r", encoding="utf-8") as f:
        rawdata = json.load(f)
    data = {}
    for post in rawdata:
        if post['id']:
            if post['id'] not in data.keys():
                data[post['id']] = {}
            if 'goose' in post.keys():
                for goose in post['goose']:
                    if goose not in data[post['id']].keys():
                        data[post['id']][goose] = 0
                    try:
                        data[post['id']][goose] = data[post['id']][goose] + int(post['goose'][goose])
                    except Exception as e:
                        print(e)
    with open('Data.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))
