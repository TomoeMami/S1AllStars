# -*- coding: utf-8 -*-
import os
import re
import json

def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    path=path.encode('utf-8')
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

def all_files_path(rootDir):                       
    for root, dirs, files in os.walk(rootDir):     # 分别代表根目录、文件夹、文件
        for file in files:                         # 遍历文件
            file_path = os.path.join(root, file)   # 获取文件绝对路径  
            filepaths.append(file_path)            # 将文件路径添加进列表
        for dir in dirs:                           # 遍历目录下的子目录
            dir_path = os.path.join(root, dir)     # 获取子目录路径
            all_files_path(dir_path)               # 递归调用
def getkwfile(flist, keyword):
    res = []
    for ff in flist:
        if keyword in ff.split('\\')[-1]:   # 切分出文件名来再判断，可以缩短判断时间
            res.append(ff)
    return res

if __name__ == "__main__":
    dirpath = '/home/riko/S1PlainTextArchive2021/'
    filepaths = []                                
    all_files_path(dirpath)
    filepath2 = getkwfile(filepaths, 'md')
    for filepath in filepath2:
        with open (filepath, 'r',encoding='UTF-8') as f:
            lines = f.readlines() 
            a = ''
            for line in lines:
                a += line.strip()
            b = a.split("*****")
            c = []
            for level in b:
                if "查看全部评分" in level:
                    c.append(level)
            res = []
            for post in c:
                data={}
                data['id'] = ''.join(re.findall(r"^####\s\s([^#]+)#", post))
                data['level'] = ''.join(re.findall(r"#####\s(\d+)#", post))
                goose = re.findall(r"\|----\|---\|---\|(.+)查看全部评分", post)
                for a in goose:
                    b = a.split("|| ")
                    gooselist = {}
                    for c in b:
                        num = ''.join(re.findall(r"\|[^-]*(-?\d{1,3})\|", c))
                        gooser = ''.join(re.findall(r"^(?:|\s)?(.+)\|[-\s]", c))
                        if(gooser):
                            if(gooser[0] == '|'):
                                gooser = gooser[2:]
                            gooselist[gooser] = (num)
                    data['goose'] = gooselist
                res.append(data)
            if(res):
                spath = ''.join(re.findall(r"\d{5,7}-\d{2,4}", filepath))
                with open('./data/'+spath+'.json',"w",encoding='utf-8') as f:
                            f.write(json.dumps(res,indent=2,ensure_ascii=False))
        with open ('test.txt','a',encoding='UTF-8') as f:
            f.write(filepath)
        #     res.append(data)
        # print(res)

