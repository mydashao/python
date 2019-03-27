'''
1.根据列表返回url http://www.tianqihoubao.com/lishi/beijing.html
2.根据url 抓取数据
3.记录
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
def get_html(url):
    headers = {'User-Agent': '', 'referer': 'link'}
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url, headers=headers)
    response.encoding = 'GBK'
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    return soup


def list_info():
    soup = get_html(url)
    url_list = soup.find('div', id="content")
    for url_list in  url_list.find_all('a'):
        list_detail=url_list.get("href")
        if list_detail[0]=="/" and list_detail[-4:] == 'html':
            weather_info(list_detail)



def weather_info(list_detail):
    count = 10003
    detail_url  = 'http://www.tianqihoubao.com/'+list_detail
    soup = get_html(detail_url)
    time.sleep(5)
    day_list = soup.find("table").find_all("td")
    for day in day_list:
        info = day.get_text().strip().replace(' ','').replace("\r\n","")
        if count%4 !=0 :
            id = 3-count%4
            mylist[-1][id] = info
            length = len(info)
            print(info, end=' ')
            for i in range(15-length):
                print('-', end=' ')
            count = count-1
        else :
            print(info)
            mylist[-1][3] = info

            mylist.append(['日期', '天气状况', '气温', '风力风向'])

            count = count-1

    time.sleep(15)
    save_to_excel(mylist)

def save_to_excel(mylist):

    headers = ('日期','天气状况','气温','风力风向')
    print(mylist)

    mylist = tablib.Dataset(*mylist, headers=headers)

    with open('D:\weather.xlsx', 'wb') as f:
        f.write(mylist.export('xlsx'))


mylist.append(['日期', '天气状况', '气温', '风力风向'])
list_info()