
import pickle
import S1Spd
import json
import os



#用于保存和读取dict
def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

#用于处理postlist,整理成基于所有相关用户的字典文档
#格式为{"postername":[发帖总数，发帖总字数，[(发帖层数，发帖内容),)],获得加鹅总数,获得扣鹅总数,加鹅总次数,加鹅总数，[(加鹅数，加鹅对象，加鹅评论)，]，扣鹅总次数,扣鹅总数，[(扣鹅数，扣鹅对象，扣鹅评论)，]]}
#加扣鹅自带符号
def get_S1_dict(postlist):
    res = {}
    for post in postlist:
        level = S1Spd.get_level(post)
        poster = S1Spd.get_postername(post)
        comment = S1Spd.get_comment(post)
        gooselist = S1Spd.get_goosedict(post)
        if poster not in res.keys():
            res[poster] = [1, len(comment), [(level,comment)], 0, 0, 0, 0, [], 0, 0, []]
        else:
            res[poster][0] += 1
            res[poster][1] += len(comment)
            res[poster][2].append((level,comment))

        for goose in gooselist.keys():
            tmp = gooselist[goose]
            if tmp[0] > 0:
                res[poster][3] += tmp[0]
                if goose not in res.keys():
                    res[goose] = [0, 0, [], 0, 0, 1, tmp[0], [(tmp[0], poster, tmp[1])],0,0,[]]
                else:
                    res[goose][5] += 1
                    res[goose][6] += tmp[0]
                    res[goose][7].append((tmp[0], poster, tmp[1]))
            else:
                res[poster][4] += tmp[0]
                if goose not in res.keys():
                    res[goose] = [0, 0, [], 0, 0, 0, 0, [], 1, tmp[0], [(tmp[0], poster, tmp[1])]]
                else:
                    res[goose][8] += 1
                    res[goose][9] += tmp[0]
                    res[goose][10].append((tmp[0], poster, tmp[1]))
    return res






if __name__ == '__main__':




    """
    to_count_list = [1,5,7,10,14,16,18,19,21,23,25,27,28,32,35,41,43,48,50,51,53,55,56,60,70,77,78,82,86,92,94,95,96,99,100,
                     101,102,103,106,107,108,118,121,122,126,130,132,133,135,138,147,157,164,168,170,174,176,182,184,185,187,
                     197,200,202,203,208,209,213,214,223,224,225,227,228,229,234,236,237,238,239,241,244,245,246,253,256,258,
                     260,266,267,272,274,275,283,284,285,293,297,305,312,314,326,328,329,330,332,328,343,344,348,353,356,362,
                     366,370,374,376,381,382,386,388,403,442,455,461,469,470,482,487,490,494,506,511,527,528,530,532,545,549,
                     551,552,558,559,560,565,581,638,647,656,677,683,685,687,689,692,693,696,712,719,721,722,723,727,728,731,732,
                     735,738,771,777,778,798,810,862,869]"""
    
    ###EXAMPLE
    link = "https://bbs.saraba1st.com/2b/thread-2015387-1-1.html"
    posts = S1Spd.get_allpost(link=link)
    print("get post finish")
    res=[]
    for post in posts:
        level = S1Spd.get_level(post)
        poster = S1Spd.get_postername(post)
        gooselist = S1Spd.get_goosedict(post)
        if(gooselist):
            data={}
            data['level'] = level
            data['id'] = poster
            data['goose'] = gooselist
            res.append(data)
    if(posts):
        with open('./data/'+str(2015501)+'.json',"w",encoding='utf-8') as f:
                f.write(json.dumps(res,indent=2,ensure_ascii=False))
    # import sy
    # sys.setrecursionlimit(10000)
    #save_obj(res,"EXAMPLE.pkl")#这个保存方法特别费递归深度，可以用上面两行代码放开限制，或者干脆重写个正常点的















