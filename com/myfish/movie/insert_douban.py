'''
1.提取citle为空和mtimerate为空
2.url=http://search.mtime.com/search/?q=Grimsby&t=1&i=0&c=290
3.提取名称和得分
http://www.cnblogs.com/themost/p/6900852.html
'''

from bs4 import BeautifulSoup
import requests
import random
import pymysql
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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


def get_empty_douban_rate():
    db = pymysql.connect(host='localhost', user='root', password='777748', port=3306, db='movie')
    cursor = db.cursor()
    sql = "SELECT title,citle,ID,release_date FROM movies WHERE douban_rate is NULL"
    #print(sql)
    try:
        cursor.execute(sql)
        while 1>0:
            data = cursor.fetchone()
            if data != None:
                title =str(data[0])
                citle = str(data[1])
                id = str(data[2])
                release_date = str(data[3])
                print(id+'-----'+title+'-----'+citle)
                get_html(title,citle,id,release_date)
                time.sleep(5)

            else:
                return '------操作完毕！！！------'
                break
    except Exception as e:
        print(e)
        return '------错误！！！------'






def get_html(title,citle,id,release_date):
    if release_date != None:
        year = release_date[0:4]
    else : year=0
    print(year)

    search_url = 'https://movie.douban.com/subject_search?search_text='+citle

    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)
    browser.get(search_url)
    #print(browser.page_source)
    list = browser.find_elements_by_class_name('title-text')
    for name in list:
        print(name.text)
        douban_year = name.text[-5:-1]
        if abs(int(year) -int(douban_year))<2:
            douban_rate = browser.find_element_by_class_name('rating_nums').text
            douban_id = browser.find_element_by_class_name('title').get_attribute('a')
            print(douban_rate)
            print(douban_id)
            return


def update_douban_rate():
    return 1

print('================开始==============')
get_empty_douban_rate()

