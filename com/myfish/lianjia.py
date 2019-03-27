'''
1. 根据url获取信息

'''

import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

import tablib

count=1
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
zj1='500'
zj2='1200'
mj1='80'
mj2='200'
j3='l3'
j4='l4'
j5='l5'
'''
l3l4l5 三四五居室
ie2有电梯 ie1没电梯
f朝向东南西北 f5南北朝向
lc 楼层 lc5顶层
url = 'bp'+zj1+'ep'+mj2+'ba'+mj1+'ea'+mj2+'l3l4l5hu0sf1lc2lc3lc5f5ie2'

'''

first_url = 'https://bj.lianjia.com/ershoufang/chaoyang/pg'
last_rul = 'co52ng0hu1hu0nb0bp500ep1200ba80ea20000l3l4l5hu0sf1lc2lc3lc5f5ie2'


mylist = []
database =[]
date1=''
date2=''

#方法1：向网站发送请求，返回HTML对象
def get_selection():
    return 1



def house_info(i):
    global count
    page_url = str(i+1)
    detail_url = first_url+page_url+last_rul
    print(detail_url)
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    #browser = webdriver.Chrome()
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(detail_url)

    #print(browser.page_source)
    list =browser.find_element_by_class_name('sellListContent').find_elements_by_class_name('LOGCLICKDATA')
    for item in list:
        url = item.find_element_by_class_name('noresultRecommend').get_attribute('href')
        id = item.find_element_by_tag_name('a').get_attribute('data-housecode')
        title = item.find_element_by_class_name('title').find_element_by_tag_name('a').text.strip()
        info1 = item.find_element_by_class_name('address').find_element_by_class_name('houseInfo').text.strip()
        a = info1.find("/")
        b = info1.find("/",a+1)
        c = info1.find("/",b+1)
        d = info1.find("/",c+1)
        e = info1.find("/",d+1)

        xiaoqu = info1[:a].strip()
        huxing = info1[a+1:b].strip()
        mianji =info1[b+1:c-2].strip()
        chaoxiang=info1[c+1:d].strip()
        zhuangxiu=info1[d+1:e].strip()
        dianti=info1[e+1:].strip()

        info2 = item.find_element_by_class_name('flood').find_element_by_class_name('positionInfo').text.strip()
        f=info2.find("/")
        g=info2.find("/",f+1)
        h=info2.find("(")

        louceng=info2[:h].strip()
        zonggao=info2[h+1:f-1].strip()
        niandai=info2[f+1:f+5].strip()
        louxing=info2[f+7:g].strip()
        diqu = info2[g+1:].strip()
        guandai = item.find_element_by_class_name('followInfo').text.strip()

        i = guandai.find("/")
        j = guandai.find("\n")
        guanzhu=guandai[:i-3]
        daikan =guandai[i+1:j-3]

        try:
            ditie =item.find_element_by_class_name('subway').text.strip()
        except:
            ditie = ''
        try:
            VR=item.find_element_by_class_name('vr').text.strip()
        except:
            VR = ''
        try:
            taxfree=item.find_element_by_class_name('taxfree').text.strip()
            taxfree = '5年'
        except:
            try:
                taxfree=item.find_element_by_class_name('five').text.strip()
                taxfree='2年'
            except:
                taxfree='不满'
        try:
            kanfang=item.find_element_by_class_name('haskey').text.strip()
        except:
            kanfang = ''
        zongjia=item.find_element_by_class_name('totalPrice').text.strip()[:-1]
        danjia=item.find_element_by_class_name('unitPrice').text.strip()[2:-4]


        print('====================' + str(count) + '====================')
        print(' 链接 :' + url)
        print(' ID :' + str(id))
        print(' 简介 :' + title)
        print(' 地区 :' + diqu)
        print(' 总价 :' + zongjia)
        print(' 单价 :' + danjia)
        print(' 详情 :')
        print(' 小区 :' + xiaoqu)
        print(' 户型 :' + huxing)
        print(' 面积 :' + mianji)
        print(' 朝向 :' + chaoxiang)
        print(' 装修 :' + zhuangxiu)
        print(' 电梯 :' + dianti)
        print(' 楼层 :' + louceng)
        print(' 总高 :' + zonggao)

        print(' 年代 :' + niandai)
        print(' 楼型 :' + louxing)
        print(' 地铁 :' + ditie)
        print(' VR :' + VR)
        print(' 购房 :' + taxfree)
        print(' 看房 :' + kanfang)
        print(' 关注 :' + guanzhu)
        print(' 带看 :' + daikan)

        mylist.append([id, title, diqu, xiaoqu, zongjia, danjia, huxing, mianji, chaoxiang, zhuangxiu,
    dianti, louceng,zonggao, niandai, louxing, ditie, VR, taxfree, kanfang, guanzhu,daikan,url])

        count=count+1


    time.sleep(10)
    save_to_excel(mylist)


def save_to_excel(mylist):

    headers = (
    'ID', 'title', 'diqu',  'xiaoqu', 'zongjia', 'danjia','huxing', 'mianji', 'chaoxiang', 'zhuangxiu',
    'dianti', 'louceng','zonggao', 'niandai', 'louxing', 'ditie', 'VR', 'taxfree', 'kanfang', 'guanzhu','daikan','url')
    #print(mylist)

    mylist = tablib.Dataset(*mylist, headers=headers)

    with open('D:\zhaofang.xlsx', 'wb') as f:
        f.write(mylist.export('xlsx'))


def total_pages():
    page_url = '1'
    detail_url = first_url+page_url+last_rul
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    # browser = webdriver.Chrome()
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(detail_url)
    house_number = int(
        browser.find_element_by_class_name('resultDes').find_element_by_class_name('total').text[3:-9].strip())
    page_number= int(get_url(house_number))
    print('----共计'+str(house_number)+'套房屋----')
    print('----共计'+str(page_number)+'页----')
    return page_number



def get_url(next_page):
    if next_page<=30:
        return 1
    else :
        return int(next_page)/30+1

total_page=total_pages()
print(total_page)
for i in range(total_page):
    print(i)
    house_info(i)
