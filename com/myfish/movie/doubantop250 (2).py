#!/usr/bin/env python
import urllib.request
from bs4 import BeautifulSoup

mylist = []
print(u'豆瓣电影TOP250:\n 序号 \t 影片名\t 评分\t 评价人数\t 评价')


def crawl(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, timeout=10)
    contents = page.read()
    soup = BeautifulSoup(contents, "html.parser")
    for tag in soup.find_all('div', class_='item'): #定义在所有item标签里的tag
        try:
            m_order = int(tag.find('em', class_='').get_text())
            m_name = tag.span.get_text()
            #global m_rating_score = float(tag.find('div', class_='star').em.get_text())
            m_ename = tag.find('div', class_='hd').span.next_sibling.next_sibling.get_text()
            #print('打印',m_ename)
            m_rating_num = tag.find('div', class_='star').span.next_sibling.next_sibling.get_text()
            m_url = tag.find('a')
            m_comments = tag.find("span", class_="inq").get_text()
        except AttributeError:
            print("%s %s %s %s %s %s" % (m_order, m_name, m_ename, m_rating_num, m_url,"NO COMMENTS"))
            mylist.append((m_order, m_name,  m_ename, m_rating_num, m_url,"NO COMMENTS"))
        else:
            print("%s %s %s %s %s %s" % (m_order, m_name, m_ename,  m_rating_num, m_url,m_comments))
            mylist.append((m_order, m_name, m_ename,  m_rating_num, m_url,m_comments))


pagenumber = []
for i in range(10):
    page_number = 25 * i
    pagenumber.append(page_number)
pagelist = list(map(str, pagenumber))

BASE_URL = 'http://movie.douban.com/top250?start='
LAST_URL = '&filter=&type='
#拼接 url start;从多少位开始 midurl：一个25的倍数
for url in [BASE_URL + MID_URL + LAST_URL for MID_URL in pagelist]:
    crawl(url)

import tablib

headers = ('m_order', 'm_name','m_ename', 'm_rating_num', 'm_url','m_comments')
mylist = tablib.Dataset(*mylist, headers=headers)
print(mylist.csv)
with open('D:\douban_TOP250.xlsx', 'wb') as f:
    f.write(mylist.xlsx)