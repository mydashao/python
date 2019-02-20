'''
1.提取citle为空和mtimerate为空
2.url=http://search.mtime.com/search/?q=Grimsby&t=1&i=0&c=290
3.提取名称和得分
http://www.cnblogs.com/themost/p/6900852.html
'''

from bs4 import BeautifulSoup
import requests
import random
import difflib

import Levenshtein

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
    count = 0
    db = pymysql.connect(host='localhost', user='root', password='777748', port=3306, db='movie')
    cursor = db.cursor()
    sql = "SELECT title,citle,ID,release_date FROM movies WHERE douban_rate is NULL "
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
                count=count+1
                print('===================='+str(count)+'====================')
                print('    '+id+' '+citle+' '+title+' ('+release_date+')')

                get_html(title,citle,id,release_date)
                time.sleep(15)

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
    #print('    ' +year)

    search_url = 'https://movie.douban.com/subject_search?search_text='+citle

    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    #browser = webdriver.Chrome(chrome_options=option)
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)
    browser.get(search_url)
    imdb_id = id
    #print(browser.page_source)
    list = browser.find_elements_by_class_name('title-text')
    for name in list:
        #print( name.text)
        douban_year = name.text[-5:-1]
        ind = name.text.find(" ")

        douban_citle = name.text[:ind]

        #if(abs(int(float(year)) -int(float(douban_year)))<1):
        if (abs(int(float(year)) -int(float(douban_year)))<1 and similar(citle,douban_citle)>0.6) :
            print('    影片名：' + citle)
            print('    豆瓣名：' + douban_citle)
            print('    影片年：' + year)
            print('    豆瓣年：' + douban_year)
            print('    相似度：' + str(similar(citle, douban_citle)))
            douban_url = name.get_attribute('href')
            index = douban_url.find("subject/")+8
            douban_id = douban_url[index:-1]

            douban_rate = browser.find_element_by_class_name('rating_nums').text
            votes = browser.find_element_by_class_name('pl').text[1:-4]
            print('    豆瓣ID :'+douban_id)
            print('    豆瓣评分:'+douban_rate)
            print('    评分人数:'+votes)
            print('    影片链接:'+douban_url)
            update_douban_rate(imdb_id,douban_id,douban_rate,votes)
            return
    update_douban_zero(imdb_id,str(-1))

def similar(citle,douban_citle):
    return Levenshtein.ratio(citle, douban_citle)


def update_douban_zero(imdb_id,douban_rate):
    db = pymysql.connect(host='localhost', user='root', password='777748', port=3306, db='movie')
    cursor = db.cursor()
    sql = "UPDATE movies SET douban_rate = " + douban_rate + " WHERE ID='" + imdb_id + "'"
    print(sql)
    print('******************未找到******************')

    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print('错误')
        print(e)

def update_douban_rate(imdb_id,douban_id,douban_rate,votes):
    db = pymysql.connect(host='localhost', user='root', password='777748', port=3306, db='movie')
    cursor = db.cursor()
    sql = "UPDATE movies SET douban_rate = "+douban_rate+" WHERE ID='"+imdb_id+"'"
    sql_douban = "UPDATE movies SET rating = "+douban_rate+" " \
                                 "   votes = "+votes+" " \
                                 " WHERE ID='"+imdb_id+"'"
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print('错误')
        print(e)

print('===================开始===================')
get_empty_douban_rate()

