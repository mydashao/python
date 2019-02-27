'''
1. 根据url获取信息

'''

import random
import requests
import time
from bs4 import BeautifulSoup
import tablib


user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    ]

#url = 'https://www.imdb.com/user/ur7858364/ratings'
url=\
'http://www.tianqihoubao.com/lishi/beijing.html'
mylist = []
database =[]
count=0
date1=''
date2=''

#方法1：向网站发送请求，返回HTML对象
def get_selection():
    return 1


def get_html(url):
    headers = {'User-Agent': '', 'referer': 'link'}
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url, headers=headers)
    response.encoding = 'GBK'
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    return soup

def house_info(list_detail):
    detail_url  = 'https://bj.lianjia.com/ershoufang/chaoyang/ng0hu1nb0ie2f5lc2lc3lc5l3l4l5ba80ea20000bp500ep1000/'
    soup = get_html(detail_url)
    time.sleep(5)
    day_list = soup.find("table").find_all("td")
    

    time.sleep(15)
    save_to_excel(mylist)