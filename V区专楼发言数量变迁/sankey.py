
import re
import json
from pathlib import Path
import os
import json

from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.commons.utils import JsCode
from pyecharts.options.global_options import InitOpts, TitleOpts
import time 

def SankeyData():
    rawdata = {}
    with open("/home/riko/S1AllStars/V区专楼发言数量变迁/A-RawData.json", "r", encoding="utf-8") as f:
        arawdata = json.load(f)
        rawdata['arawdata'] = arawdata
    with open("/home/riko/S1AllStars/V区专楼发言数量变迁/B-RawData.json", "r", encoding="utf-8") as f:
        brawdata = json.load(f)
        rawdata['brawdata'] = brawdata
    with open("/home/riko/S1AllStars/V区专楼发言数量变迁/C-RawData.json", "r", encoding="utf-8") as f:
        crawdata = json.load(f)
        rawdata['crawdata'] = crawdata
    with open("/home/riko/S1AllStars/V区专楼发言数量变迁/H-RawData.json", "r", encoding="utf-8") as f:
        hrawdata = json.load(f)
        rawdata['hrawdata'] = hrawdata
    with open("/home/riko/S1AllStars/V区专楼发言数量变迁/M-RawData.json", "r", encoding="utf-8") as f:
        mrawdata = json.load(f)
        rawdata['mrawdata'] = mrawdata
    with open("/home/riko/S1AllStars/V区专楼发言数量变迁/V-RawData.json", "r", encoding="utf-8") as f:
        vrawdata = json.load(f)
        rawdata['vrawdata'] = vrawdata
    timedatadict = {}
    for datakey in rawdata.keys():
        timedatadict[datakey] = {}
        for post in rawdata[datakey]:
            postintime = int(time.mktime(time.strptime(post['time'],"%Y-%m-%d %H:%M")))
            # if postintime%2592000 :
            #     postintime = postintime - postintime%2592000
            posttime = time.strftime("%Y-%m", time.localtime(postintime))
            postid = post['id']
            if posttime not in timedatadict[datakey].keys():
                timedatadict[datakey][posttime] = {}
            if postid not in timedatadict[datakey][posttime].keys():
                timedatadict[datakey][posttime][postid] = 1
            else:
                timedatadict[datakey][posttime][postid] = 1 + timedatadict[datakey][posttime][postid]
    data = {}
    for datakey in timedatadict.keys():
        for posttime in timedatadict[datakey].keys():
            if posttime not in data.keys():
                data[posttime] = {}
            data[posttime][datakey] = {}
            for ids in timedatadict[datakey][posttime].keys():
                if timedatadict[datakey][posttime][ids] > 15 :
                    data[posttime][datakey][ids] = timedatadict[datakey][posttime][ids]
     
    with open('/home/riko/S1AllStars/V区专楼发言数量变迁/Sankey-DataDict.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))

def MakeNodes():
    with open('/home/riko/S1AllStars/V区专楼发言数量变迁/Sankey-DataDict.json', "r", encoding="utf-8") as f:
        datadict = json.load(f)
    idict={}
    for datakey in datadict.keys():
        for posttime in datadict[datakey].keys():
            for ids in datadict[datakey][posttime].keys():
                if ids in idict.keys():
                    idict[ids] = idict[ids] + datadict[datakey][posttime][ids]
                else:
                    idict[ids] = datadict[datakey][posttime][ids]
    data = []
    nodes = []
    links = []
    translatedict = {"vrawdata":"v综","arawdata":"a综","brawdata":"b综","crawdata":"c综","mrawdata":"m综","hrawdata":"h综"}
    colordict = {"vrawdata":"#b8bb26","arawdata":"#fabd2f","brawdata":"#83a598","crawdata":"#d3869b","mrawdata":"#8ec07c","hrawdata":"#fe8019"}
    namedict = {}
    for month in sorted(datadict.keys()):
        if month != 'ids':
            for threads in datadict[month].keys():
                threadcount = 0
                for reply in datadict[month][threads].keys():
                    if (reply not in namedict.keys()) and (datadict[month][threads][reply] > 30):
                        snode = {}
                        snode['name'] = reply
                        snode['symbolSize'] = idict[reply] / 300
                        snode['value'] = idict[reply]
                        snode['draggable'] = False
                        snode['itemStyle'] = {"color" : "#928374"}
                        c = snode
                        nodes.append(c)
                        namedict[reply] = 1
                    threadcount = threadcount + datadict[month][threads][reply]
                snode = {}
                snode['name'] = translatedict[threads] + ' ' + month
                if (threadcount / 300) < 0.1:
                    snode['symbolSize'] = 0.1
                else:
                    snode['symbolSize'] = threadcount / 300  
                snode['value'] = threadcount
                snode['draggable'] = False
                snode['itemStyle'] = {"color" : colordict[threads]}

                c = snode
                nodes.append(c)

    # threadlist1 = ["vrawdata","arawdata","brawdata","crawdata","mrawdata","hrawdata"]
    # threadlist2 = threadlist1
    # lastmonth = ''
    # for month in sorted(datadict.keys()):
    #     if lastmonth:
    #         for thread1 in datadict[lastmonth].keys():
    #             slink = {}
    #             slink['source'] = translatedict[thread1] + ' ' + lastmonth
    #             slink['target'] = translatedict[thread1] + ' ' + month
    #             slink['value'] = 0
    #             slink['lineStyle'] = {}
    #             slink['lineStyle']['width'] = 5
    #             d = slink
    #             links.append(d)
    #     lastmonth = month
    for month in sorted(datadict.keys()):
        for threads in datadict[month].keys():
            for reply in datadict[month][threads].keys():
                if datadict[month][threads][reply] > 30:
                    slink = {}
                    slink['source'] = reply
                    slink['target'] = translatedict[threads] + ' ' + month
                    slink['value'] = datadict[month][threads][reply]
                    slink['lineStyle'] = {}
                    slink['lineStyle']['width'] = datadict[month][threads][reply]/900
                    slink['lineStyle']['color'] = 'rgba(7,102,120,0.4)'
                    d = slink
                    links.append(d)
    data.append(nodes)
    data.append(links)
    with open('/home/riko/S1AllStars/V区专楼发言数量变迁/Sankey-Data.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(data,indent=2,ensure_ascii=False))

def Render():


    with open("/home/riko/S1AllStars/V区专楼发言数量变迁/Sankey-Data.json", "r", encoding="utf-8") as f:
        j = json.load(f)
    nodes, links = j
    c = (
        Graph(init_opts=opts.InitOpts(page_title="S1V区发言关系网"))
        .add(
            "",
            nodes,
            links,
            repulsion=40000,
            edge_length=[1500,1000],
            is_draggable = False,
            layout = 'force',
            # is_focusnode=False,
            linestyle_opts=opts.LineStyleOpts(curve=0.2),
            label_opts=opts.LabelOpts(
                # is_show=True,
                is_show=True,
                # formatter='{c}'
                ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True
            )
            # edge_symbol='arrow',
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="V区专楼发言关系网",
            subtitle="仅统计某月在某专楼发言次数超过30次的用户"),
            )
        .render("/home/riko/S1AllStars/V区专楼发言数量变迁/index.html")
    )

if __name__ == "__main__":

    # SankeyData()
    MakeNodes()
    Render()