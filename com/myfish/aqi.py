'https://www.aqistudy.cn/historydata/daydata.php?city=%E5%8C%97%E4%BA%AC&month=201402'

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
from selenium import webdriver



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
'https://www.aqistudy.cn/historydata/daydata.php?city=%E5%8C%97%E4%BA%AC&month=201312'
mylist = []
database =[]
count=0
date1=''
date2=''


def get_date():
    soup = get_html(url)
    url_list = soup.find('ul', class_='unstyled1')
    for url_list in  url_list.find_all('a'):
        data_list=url_list.get("href")[-6:]
        aqi_info(data_list)

        # if list_detail[0]=="/" and list_detail[-4:] == 'html':
        #     # weather_info(list_detail)

#方法1：向网站发送请求，返回HTML对象
def get_html(url):
    headers = {'User-Agent': '', 'referer': 'link'}
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url, headers=headers)
    response.encoding = 'GBK'
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    return soup

def aqi_info(data_list):
    detail_url  = 'https://www.aqistudy.cn/historydata/daydata.php?city=北京&month='+data_list
    print(detail_url)
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(detail_url)

    time.sleep(15)

    # print(browser.page_source)
    list = browser.find_elements_by_tag_name('td')
    count = 0

    for detail in list:

        info = detail.text
        if (count+1) % 9!=0:
            mylist[-1][count] = info
            count=count+1
        else:
            mylist[-1][8] = info
            print(mylist[-1])
            count = 0
            mylist.append(['日期', 'AQI', '质量等级', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3_8h'])

    save_to_excel(mylist)

def save_to_excel(mylist):

    headers = ('日期', 'AQI', '质量等级', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3_8h')
    print(mylist)

    mylist = tablib.Dataset(*mylist, headers=headers)

    with open('D:\AQI.xlsx', 'wb') as f:
        f.write(mylist.export('xlsx'))


mylist.append(['日期', 'AQI', '质量等级', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3_8h'])

get_date()