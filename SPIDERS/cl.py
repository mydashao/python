# https://cl.d35.xyz/thread0806.php?fid=15&search=&page=6
#
# https://cl.d35.xyz/htm_data/15/1901/3412435.html
#
# http://www.rmdown.com/link.php?hash=19115e683ef7da964d16428b88124dd649410aa7d0e
#
# http://www.rmdown.com/download.php?reff=226597&ref=19117b617b882778ab8c51e33ac6b0d55716c8d9041
# http://www.rmdown.com/download.php?reff=477953&ref=1916ccc61154809e61ce087c1d19f10a6e4733c06c1
# http://www.rmdown.com/download.php?reff=164020&ref=19115e683ef7da964d16428b88124dd649410aa7d0e
# http://www.rmdown.com/download.php?reff=408398&ref=19115e683ef7da964d16428b88124dd649410aa7d0e


#!/usr/bin/env python
import urllib.request
from bs4 import BeautifulSoup
import requests
import time
import tablib
import random


mylist = ['MP1','MP2','MP3','JULIA','園田','MP6','MP7','MP8','MP9']

user_agent_list = [ "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]


def crawl(url):
    headers = {'User-Agent':'','referer':'link'}
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url, headers=headers)
    time.sleep(20)

    response.encoding ='GBK'
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all('h3'): #定义在所有item标签里的tag
        try:
            content = tag.get_text()
            herf =tag.find('a')['href']

           # print(herf)
            #print(len(mylist))
            for find in range(len(mylist)):
                #print(mylist[find])
                if mylist[find] in content:
                    #print('转到get——info')
                    get_info(content,herf)


        except :
            print('ERROR')
            # mylist.append((m_order, m_name,  m_ename, m_rating_num, m_url,"NO COMMENTS"))
        # else:
            # print("%s %s %s %s %s %s" % (m_order, m_name, m_ename,  m_rating_num, m_url,m_comments))
            # mylist.append((m_order, m_name, m_ename,  m_rating_num, m_url,m_comments))
            # #print(m_url)
            # #print(url.index(str))


def get_info(content,href):
    print('  '+content)
    url_content = "https://cl.d35.xyz/"+href
    print('  '+url_content)

BASE_URL = 'https://cl.d35.xyz/thread0806.php?fid=15&search=&page='
for LAST_URL in range(20):
    url =BASE_URL+str(LAST_URL+1)
    print(url)
    crawl(url)


# tables = ('m_order', 'm_name', 'm_ename', 'm_rating_num', 'm_url', 'm_comments')
# mylist = tablib.Dataset(*mylist, headers=tables)
# print(mylist.csv)
# with open('D:\douban250.xlsx', 'wb') as f:
#     f.write(mylist.xlsx)

