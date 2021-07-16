import requests
from bs4 import BeautifulSoup as bs
import re

#对S1进行一个虫的爬！

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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47',
        }
    strhtml = requests.get(link, headers=headers)
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

#返回加鹅扣鹅字典
def get_goosedict(post):
    if len(post.find_all("a",title = "查看全部评分",class_ = "xi2")) ==0:
        return {}
    gooselink = "https://bbs.saraba1st.com/2b/"+post.find_all("a",title = "查看全部评分",class_ = "xi2")[0]["href"]
    gooselist = requests.get(gooselink)
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

#返回评论文字内容 可控制是否包含引用
def get_comment(post,include_quote = False):
    try:
        comment = post.find_all("td", class_="t_f")[0]
        if include_quote is False:
            comment = re.sub('\<blockquote\>[\S\s]*?\</blockquote\>', '', str(comment))
        comment = re.sub('\<.*?\>', '', str(comment))
    except:
        comment = ""
    return comment





if __name__ == '__main__':

    
    ###EXAMPLE
    link = "https://bbs.saraba1st.com/2b/thread-2013586-1-1.html"
    """
    while True:
        postlist,link = get_postlist(link)
        for post in postlist:
            print(get_postername(post))
            print(get_level(post))
            print(get_comment(post))
            print(get_goosedict(post))
            print("____________________________________________________")
        if link==-1:
            break
    """
    posts_by_someone = get_allpost(link,posters=["RexJax"])
    for post in posts_by_someone:
        print(get_postername(post))
        print(get_level(post))
        print(get_comment(post))
        print(get_goosedict(post))
        print("____________________________________________________")













