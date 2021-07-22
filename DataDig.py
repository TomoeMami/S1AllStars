# -*- coding: utf-8 -*-
import json
import os
import copy

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

def FilData():
    with open('RawData.json', "r", encoding="utf-8") as f:
        rawdata = json.load(f)
    data = {}
    for post in rawdata:
        if post['id']:
            if post['id'] not in data.keys():
                data[post['id']] = {}
                data[post['id']]['size'] = 0
                data[post['id']]['abssize'] = 0
                data[post['id']]['goose'] = {}
            if 'goose' in post.keys():
                for goose in post['goose']:
                    if goose:
                        if goose not in data[post['id']]['goose'].keys():
                            data[post['id']]['goose'][goose] = 0
                        try:
                            data[post['id']]['goose'][goose] = data[post['id']]['goose'][goose] + int(post['goose'][goose])
                            data[post['id']]['size'] = data[post['id']]['size'] + int(post['goose'][goose])
                            data[post['id']]['abssize'] = data[post['id']]['abssize'] + abs(int(post['goose'][goose]))
                        except Exception as e:
                            print(e)
    with open('DataDict.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))

def MakeNodes():
    with open('DataDict.json', "r", encoding="utf-8") as f:
        datadict = json.load(f)
    nodes = []
    links = []
    data = []
    for key in datadict.keys():
        if datadict[key]['abssize'] > 10:
            snode = {}
            snode['name'] = key
            snode['symbolSize'] = datadict[key]['abssize'] /10
            snode['value'] = datadict[key]['size']
            snode['draggable'] = True
            if datadict[key]['size'] <0 :
                snode['itemStyle'] = {"color" : '#d65d0e'}
            else:
                snode['itemStyle'] = {"color" : '#689d6a'}
            if datadict[key]['size'] < -9:
                snode['category'] = datadict[key]['category'] = 1
            elif datadict[key]['size'] > 9:
                snode['category'] = datadict[key]['category'] = 3
            else:
                snode['category'] = datadict[key]['category'] = 2
            c = snode #防止直接传递变量
            nodes.append(c)
        for goose in datadict[key]['goose']:
            width = abs(datadict[key]['goose'][goose])
            if width > 3:
                slink = {}
                slink['source'] = goose
                slink['target'] = key
                slink['lineStyle'] = {}
                slink['value'] = datadict[key]['goose'][goose]
                slink['lineStyle']['width'] = abs(datadict[key]['goose'][goose])/50
                if datadict[key]['goose'][goose] >0 :
                    slink['lineStyle']['color'] = 'rgba(7,102,120,0.7)'
                else:
                    slink['lineStyle']['color'] = 'rgba(175,58,3,0.7)'
                slink['lineStyle']['edge_label'] = str(datadict[key]['goose'][goose])
                d = slink
                links.append(d)
    data.append(nodes)
    data.append(links)
    with open('Data.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))

if __name__ == "__main__":

    # Merge()
    
    FilData()

    MakeNodes()

