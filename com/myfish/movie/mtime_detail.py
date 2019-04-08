#!/usr/bin/env python

"""
mtime 页面中演员格式
#<dl class="main_actor">
                        <dd>
                            <a class="__r_c_" pan="M14_Movie_Overview_Actor_1" href="http://people.mtime.com/1719883/" target="_blank" title="基特&#183;哈灵顿 Kit Harington"><img src="http://img31.mtime.cn/ph/2014/03/14/153029.56094575_50X50.jpg" width="50" height="50" alt="基特&#183;哈灵顿 Kit Harington" class="per"></a>
                            <p class="__r_c_" pan="M14_Movie_Overview_Actor_1">
                                <a href="http://people.mtime.com/1719883/" target="_blank" rel="v:starring">基特&#183;哈灵顿</a>
                            </p>
                                <p class="__r_c_" pan="M14_Movie_Overview_Actor_1"><a href="http://people.mtime.com/1719883/" target="_blank" rel="v:starring">Kit Harington</a></p>
                                    <p class="__r_c_" pan="M14_Movie_Overview_Actor_1">饰&nbsp;Milo</p>
<img src="http://img31.mtime.cn/mg/2014/08/15/101734.66960707_50X50X4.jpg" width="50" height="50" alt="Milo" class="cha __r_c_" pan="M14_Movie_Overview_Role_1">                        </dd>
                    </dl>
"""



import urllib.request
from bs4 import BeautifulSoup

mylist = []
print(u'mtimetop100:\n 序号 \t 影片名\t 评分\t 评价人数\t 评价')


def crawl(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, timeout=10)
    contents = page.read()
    soup = BeautifulSoup(contents, "html.parser")
    Mname = soup.find('h1',property="v:itemreviewed").get_text()
    print(Mname)
    #mylist.append(Mname)
    for tag in soup.find_all('div', class_='pic_58'): #定义在所有item标签里的tag
        try:
           # print(tag)

            m_order = tag.find('p').get_text()
            m_name = tag.find('p').get_text()
            #global m_rating_score = float(tag.find('div', class_='star').em.get_text())
            m_ename = tag.find('p').get_text()
            #print('打印',m_ename)
            m_rating_num = tag.find('p').get_text()
            m_url = tag.find('p').get_text()
            m_comments = tag.find('p').get_text()
        except AttributeError:
            print("%s %s %s %s %s %s %s" % (Mname ,m_order, m_name, m_ename, m_rating_num, m_url,"NO COMMENTS"))
            mylist.append((Mname,m_order, m_name,  m_ename, m_rating_num, m_url,"NO COMMENTS"))
        else:
            print("%s %s %s %s %s %s %s" % (Mname ,m_order, m_name, m_ename,  m_rating_num, m_url, m_comments))
            mylist.append((Mname,m_order, m_name, m_ename,  m_rating_num, m_url,m_comments))

pagenumber = []
#for i in range(1):
   # page_number = 25 * i
    #pagenumber.append(page_number)
#pagelist = list(map(str, pagenumber))
pagelist = ["11234","13367","11925","10288","11319","10970","83276","45997","10746","93049","125424","51119","63105","92909","81377","112254","107122","14865","51378","11404","16682","13695","11809","11211","11245","11962","10578","10717","11421","13187","12428","79055","11970","11403","10468","46125","86897","11600","205222","10637","13557","13700","10895","12502","156495","15431","45538","143329","13353","11249","11072","142064","13877","10834","11329","106313","48615","10957","52414","11526","12493","12142","10368","78592","108756","51236","10429","10339","24803","11332","148531","122493","13594","149859","12383","11717","41005","52841","10380","11230","10246","10364","15783","11655","10606","12467","207131","108622","12218","10674"]

BASE_URL = 'http://movie.mtime.com/'
LAST_URL = '/fullcredits.html'
#拼接 url start;从多少位开始 midurl：一个25的倍数
for url in [BASE_URL + MID_URL + LAST_URL for MID_URL in pagelist]:
   uu ='http://movie.mtime.com/130079/fullcredits.html'
   crawl(url)

import tablib

headers = ('1', '2','3', '4', '5','6','7')
print(mylist)
mylist = tablib.Dataset(*mylist, headers=headers)
print(mylist.csv)
with open('D:\mtimedetail.xlsx', 'wb') as f:
    f.write(mylist.xlsx)