#!/usr/bin/env python
import urllib.request
from bs4 import BeautifulSoup

mylist = []
print(u'豆瓣电影TOP250:\n 序号 \t 影片名\t 评分\t 评价人数\t 评价')


def crawl(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, timeout=60)
    contents = page.read()
    soup = BeautifulSoup(contents, "html.parser")
    for tag in soup.find_all('div', class_='info'): #定义在所有item标签里的tag
        try:
            m_name = tag.find('b').get_text()
            m_id = tag.find('a')

            m_year = tag.find('span', class_='year_type').get_text()
            #global m_rating_score = float(tag.find('div', class_='star').em.get_text())
            m_director= tag.find('div', class_='secondary').get_text()
            #print('打印',m_ename)
            m_actor= tag.find('div', class_='secondary').next_sibling.next_sibling.get_text()
            m_comments = tag.find("div", class_="item_description").get_text()
        except AttributeError:
            print("%s %s %s %s %s %s" % (m_id, m_year,   m_name, m_director, m_actor,"NO COMMENTS"))
            mylist.append((m_id, m_year,   m_name, m_director, m_actor,m_comments))
        else:
            print("%s %s %s %s %s %s" % (m_id, m_year,   m_name, m_director, m_actor,"NO COMMENTS"))
            mylist.append((m_id, m_year,   m_name, m_director, m_actor,m_comments))


pagenumber = []
for i in range(11):
    page_number = 1 * i+1
    pagenumber.append(page_number)
pagelist = list(map(str, pagenumber))


BASE_URL = 'http://www.imdb.com/user/ur7858364/ratings?start='
LAST_URL = '01&view=detail&sort=ratings_date:desc'
#拼接 url start;从多少位开始 midurl：一个25的倍数
for url in [BASE_URL + MID_URL + LAST_URL for MID_URL in pagelist]:
    print(url)
    crawl(url)

import tablib

headers = ('m_id', 'm_year','m_name', 'm_director', 'm_actor','m_comments')
mylist = tablib.Dataset(*mylist, headers=headers)
print(mylist.csv)
with open('D:\imdbactor.xlsx', 'wb') as f:
    f.write(mylist.xlsx)