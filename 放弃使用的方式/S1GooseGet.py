import json
import os
import requests
from bs4 import BeautifulSoup as bs
import re
import pickle

def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

#返回加鹅扣鹅字典
def get_goosedict(post):
    if len(post.find_all("a",title = "查看全部评分",class_ = "xi2")) ==0:
        return {}
    #cookie_str1 = os.getenv('S1_COOKIE')
    cookie_str1=r'_uab_collina=157521263402491058392383; _uab_collina=160139195432419598077899; _ga=GA1.2.704367596.1575212634; __yjs_duid=1_117cd3da16f3e129d318c45727b9c1261619277697414; UM_distinctid=17a38bf79fece-0ce16632fb85de-7a697d6e-1fa400-17a38bf79ffe06; __gads=ID=1da95451769de448-22144772f5c90086:T=1624449793:RT=1624449793:S=ALNI_MbVJIL81-RGOiZPSyqbI-rtRUqZrA; CNZZDATA1260281688=1391404437-1606917668-%7C1624685934; B7Y9_2132_saltkey=EamMdYmy; B7Y9_2132_lastvisit=1625755409; B7Y9_2132_auth=26cboJq7EsEz7XY%2Fg2SKxU2YF%2B7zskb62dgxHbFtyN59KJCvpF6KrLmvN8wj9w6XHO1C1x4cDWdOJjdFi2buSx9L1cU; B7Y9_2132_lastcheckfeed=523536%7C1625759061; B7Y9_2132_atlist=489501%2C246574%2C17139%2C179449%2C529710%2C527584; B7Y9_2132_smile=1465D2; B7Y9_2132_pc_size_c=0; B7Y9_2132_yfe_in=1; B7Y9_2132_ulastactivity=2c8dZSpbe6b2GoTyl8fcVRtUa1qE6bXLE45v0O0%2BJpWGYlSUYvwp; B7Y9_2132_visitedfid=75D151D6D51D4D50D135D74D48D83; B7Y9_2132_sid=OCdMUy; B7Y9_2132_lip=113.249.242.27%2C1626369068; B7Y9_2132_st_t=523536%7C1626369331%7C7e71b8edad3eec0ccd14a1f455c44aee; B7Y9_2132_forum_lastvisit=D_48_1616318732D_55_1616323284D_27_1616391719D_77_1621179285D_83_1624723236D_6_1626019583D_4_1626019587D_50_1626271306D_51_1626350630D_151_1626368868D_75_1626369331; B7Y9_2132_popadv=a%3A0%3A%7B%7D; B7Y9_2132_sendmail=1; B7Y9_2132_checkpm=1; B7Y9_2132_lastact=1626369332%09forum.php%09ajax'
    cookie_str = repr(cookie_str1)[1:-1]
    # #把cookie字符串处理成字典，以便接下来使用
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47',
        }
    gooselink = "https://bbs.saraba1st.com/2b/"+post.find_all("a",title = "查看全部评分",class_ = "xi2")[0]["href"]
    gooselist = requests.get(gooselink,headers=headers,cookies=cookies)
    gooselist = bs(gooselist.text,"lxml")
    gooselist = gooselist.find_all("div", class_="c floatwrap")[0].find_all("tr")[1:]
    res = {}
    for goose in gooselist:
        attr = goose.find_all('td')
        num = int(attr[0].string[4:-1])
        gooser = attr[1].string
        comment = attr[-1].string
        '''
        if comment is None:
            comment =  ""
        res[gooser] = (num,comment)'''
        res[gooser] = (num)
    return res

#返回一个post的楼层数 int
def get_level(post):
    match = re.search("<em>[0-9]+</em>",str(post))
    if match is None:
        return 1
    else:
        return int(match.group()[4:-5])

#返回一个post的作者名
def get_postername(post):
    return str(post.find_all("div", class_ = "authi")[0].a.string)

#输入一个帖子地址，返回这个帖子，及这个帖子后面所有页面的楼的postlist，可控制筛选
#levels是int list，posters是str list，分别控制楼层数和作者名
def get_allpost(link,levels = None,posters = None):
    res = []
    while True:
        postlist,link = get_postlist(link)
        for post in postlist:
            if levels is not None and get_level(post) not in levels:
                continue
            if posters is not None and get_postername(post) not in posters:
                continue
            res.append(post)
        if link == -1:
            break
    return res

#输入一个帖子地址，返回这个页面所有楼(post)的html节点列表和下一页的link,如果没有下一页的话nxt返回-1
def get_postlist(link):
    #cookie_str1 = os.getenv('S1_COOKIE')
    cookie_str1=r'_uab_collina=157521263402491058392383; _uab_collina=160139195432419598077899; _ga=GA1.2.704367596.1575212634; __yjs_duid=1_117cd3da16f3e129d318c45727b9c1261619277697414; UM_distinctid=17a38bf79fece-0ce16632fb85de-7a697d6e-1fa400-17a38bf79ffe06; __gads=ID=1da95451769de448-22144772f5c90086:T=1624449793:RT=1624449793:S=ALNI_MbVJIL81-RGOiZPSyqbI-rtRUqZrA; CNZZDATA1260281688=1391404437-1606917668-%7C1624685934; B7Y9_2132_saltkey=EamMdYmy; B7Y9_2132_lastvisit=1625755409; B7Y9_2132_auth=26cboJq7EsEz7XY%2Fg2SKxU2YF%2B7zskb62dgxHbFtyN59KJCvpF6KrLmvN8wj9w6XHO1C1x4cDWdOJjdFi2buSx9L1cU; B7Y9_2132_lastcheckfeed=523536%7C1625759061; B7Y9_2132_atlist=489501%2C246574%2C17139%2C179449%2C529710%2C527584; B7Y9_2132_smile=1465D2; B7Y9_2132_pc_size_c=0; B7Y9_2132_yfe_in=1; B7Y9_2132_ulastactivity=2c8dZSpbe6b2GoTyl8fcVRtUa1qE6bXLE45v0O0%2BJpWGYlSUYvwp; B7Y9_2132_visitedfid=75D151D6D51D4D50D135D74D48D83; B7Y9_2132_sid=OCdMUy; B7Y9_2132_lip=113.249.242.27%2C1626369068; B7Y9_2132_st_t=523536%7C1626369331%7C7e71b8edad3eec0ccd14a1f455c44aee; B7Y9_2132_forum_lastvisit=D_48_1616318732D_55_1616323284D_27_1616391719D_77_1621179285D_83_1624723236D_6_1626019583D_4_1626019587D_50_1626271306D_51_1626350630D_151_1626368868D_75_1626369331; B7Y9_2132_popadv=a%3A0%3A%7B%7D; B7Y9_2132_sendmail=1; B7Y9_2132_checkpm=1; B7Y9_2132_lastact=1626369332%09forum.php%09ajax'
    cookie_str = repr(cookie_str1)[1:-1]
    # #把cookie字符串处理成字典，以便接下来使用
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47',
        }
    strhtml = requests.get(link, headers=headers,cookies=cookies)
    soup = bs(strhtml.text, 'lxml')
    nxt = soup.find_all("a", href=True, class_="nxt")
    if len(nxt)!=0:
        nxt = "https://bbs.saraba1st.com/2b/"+nxt[0]["href"]
    else:
        nxt = -1
    try:
        soup = soup.body.find_all("div", id='ct')[0].find_all("div", id="postlist")[0]
        postlist = soup.find_all("div", id=re.compile("post_[0-9]+"))
    except Exception:
        pass
        postlist = []
    return postlist,nxt

if __name__ == '__main__':

    # 设置请求头
    while True:
        try:
            threads = load_obj("threadids.pkl")
            new_threads = threads
            for threadid in threads:
                link = "https://bbs.saraba1st.com/2b/thread-"+str(threadid)+"-1-1.html"
                posts = get_allpost(link=link)
                print(len(new_threads))
                res=[]
                for post in posts:
                    gooselist = get_goosedict(post)
                    if(gooselist):
                        level = get_level(post)
                        poster = get_postername(post)
                        data={}
                        data['level'] = level
                        data['id'] = poster
                        data['goose'] = gooselist
                        res.append(data)
                if(posts):
                    with open('./data/'+str(threadid)+'.json',"w",encoding='utf-8') as f:
                            f.write(json.dumps(res,indent=2,ensure_ascii=False))
                with open('./breakpoint.txt',"w",encoding='utf-8') as f:
                        f.write(str(threadid))
                new_threads.remove(threadid)
                save_obj(new_threads,"threadids.pkl")
        except Exception:
            pass