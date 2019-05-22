'''
1. 根据url获取信息

'''

import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql

import tablib
import time

xiaoqu_chengjiao_sum = 0
count=1
chengjiao_count =1
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

dewaixuequ_=("madian1",'jiaodaokou','liupukang','deshengmen')
zizhu_=("huixinxijie","hepingli","xibahe","anzhen1","guozhan1","taiyanggong","shaoyaoju","yayuncun", "yayuncunxiaoying")

# 筛选区县还是区域
DIS_LIST = zizhu_
EXCEL_NAME = 'zizhu_'
current_time = time.strftime("%Y_%m_%d", time.localtime(time.time()))
house_number = 0



first_url = 'https://bj.lianjia.com/xiaoqu/'
middle_url = "/pg"


xiaoqu_list = []
chengjiao_list = []
database =[]
date1=''
date2=''

def main():
    loop_district()

# 根据DIS_LIST区域列表中的区域，查询列表区域的所有小区
def loop_district():
    # 循环查询district_list中的各个区域
    for dis in DIS_LIST:
        district_first_url = first_url+dis
        print("区域："+dis)
        # 通过total_pages方法计算当前区域有多少个房源，多少页，返回总页数
        total_page=xiaoqu_total_pages(district_first_url)
        # 循环查询每页信息
        for i in range(total_page):
            xiaoqu_info(dis,i)

# 计算小区列表的页数
def xiaoqu_total_pages(url):

    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    # browser = webdriver.Chrome()
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(url)
    global house_number
    house_number = int(
        browser.find_element_by_class_name('content').find_element_by_class_name('total').text[3:-3].strip())
    page_number= int(get_url(house_number))
    print('----共计'+str(house_number)+'个小区----')
    print('----共计'+str(page_number)+'页----')
    return page_number

# 计算页数的算法
def get_url(next_page):
    if next_page<=30:
        return 1
    else :
        return int(next_page)/30+1

# 抓取小区具体情况
def xiaoqu_info(dis, i):
    global count
    page_url = str(i + 1)

    detail_url = first_url + dis + middle_url + page_url

    print(detail_url)
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    # browser = webdriver.Chrome()
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(detail_url)

    # print(browser.page_source)
    list = browser.find_elements_by_css_selector('.clear.xiaoquListItem ')
    for item in list:
        score = 0
        try:
            url = item.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute('href')
        except:
            url = ''
        try:
            id = 'c' + url[30:-1]
        except:
            id = None

        title = item.find_element_by_class_name('title').find_element_by_tag_name('a').text.strip()

        try:
            chengjiao = item.find_element_by_class_name('houseInfo').text.strip()[0:-7]
        except:
            chengjiao = ''

        diqu = item.find_element_by_class_name('positionInfo').find_element_by_class_name('bizcircle').text.strip()
        chengqu = item.find_element_by_class_name('positionInfo').find_element_by_class_name('district').text.strip()

        junjia = item.find_element_by_class_name('totalPrice').text.strip()[0:-4]
        zaishou = item.find_element_by_class_name('xiaoquListItemSellCount').text.strip()[0:-7]

        print('========' + diqu + '========' + str(count) + '========' + str(house_number - count) + '========')

        print('  简介 :' + id, title, diqu, chengqu)
        print('  价格 :' + junjia, chengjiao, zaishou)

        if 1==1:
            xiaoqu_list.append([id, url, title, dis, diqu, chengqu, chengjiao, junjia, zaishou])
            total_page = xiaoqu_total(id)
            # 循环查询每页信息
            for i in range(total_page):
                # 循环查询小区列表中每个小区的成交记录
                xiaoqu_chengjiao(title, id, i)
                chengjiao_save_to_excel(id, chengjiao_list)
                time.sleep(10)

            xiaoqu_save_to_excel(dis, xiaoqu_list)

        count = count + 1

    time.sleep(10)

# 根据小区id查询小区成交数量
def xiaoqu_total(id):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=option)
    url = 'https://bj.lianjia.com/chengjiao/'+id
    browser.get(url)
    # print(browser.page_source)
    global xiaoqu_chengjiao_sum
    xiaoqu_chengjiao_sum = int(browser.find_element_by_class_name('resultDes').text.strip().strip()[3:-12])

    page_number= int(get_url(xiaoqu_chengjiao_sum))
    print('  成交 :'+str(xiaoqu_chengjiao_sum)+'套房屋 共计'+str(page_number)+'页')
    return page_number

# 根据小区id查询小区成交记录
def xiaoqu_chengjiao(title,id,i):
    page_url = str(i+1)

    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=option)
    url = 'https://bj.lianjia.com/chengjiao/' + id+'/pg'+page_url
    browser.get(url)
    # xiaoqu_info = browser.find_element_by_class_name('agentCardDetail').text.strip().replace()
    # print('    ',title,xiaoqu_info)
    list = browser.find_element_by_class_name('listContent').find_elements_by_tag_name('li')
    for item in list:
        score = 0
        try:
            url = item.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute('href')
        except:
            url = ''
        try:
            id = 'LJ' + url[33:-1]
        except:
            id = None

        title = item.find_element_by_class_name('title').text.strip()

        try:
            address = item.find_element_by_class_name('houseInfo').text.strip()
        except:
            address = ''
        try:
            guapai = item.find_element_by_class_name('dealCycleTxt').text.strip()
            # zhouqi = item.find_element_by_class_name('dealCycleTxt').text.strip()
        except:
            guapai = ''

        try:
            chengjiao = item.find_element_by_class_name('totalPrice').text.strip()
        except:
            chengjiao = ''


        lou = item.find_element_by_class_name('positionInfo').text.strip()

        fang = item.find_element_by_class_name('houseIcon').text.strip()
        dealdate =item.find_element_by_class_name('dealDate').text.strip()
        global chengjiao_count
        global xiaoqu_chengjiao_sum
        print('     ',chengjiao_count,xiaoqu_chengjiao_sum,title,address,guapai,chengjiao,fang,lou,dealdate)
        chengjiao_count=chengjiao_count+1
        xiaoqu_chengjiao_sum = xiaoqu_chengjiao_sum-1
        chengjiao_list.append([id, url, title, address, guapai,chengjiao, fang, lou, dealdate])


# 小区列表保存到excel
def xiaoqu_save_to_excel(dis, xiaoqu_list):
    headers = ('ID', 'url', '小区', '地区', '地区2', '城区', '成交', '均价', '在售')
    xiaoqu_list = tablib.Dataset(*xiaoqu_list, headers=headers)

    with open('D:\Xiaoqu2_' + EXCEL_NAME + current_time + '.xlsx', 'wb') as f:
        f.write(xiaoqu_list.export('xlsx'))


# 成交列表保存到excel
def chengjiao_save_to_excel(dis, chengjiao_list):
    headers = ('id', 'url', 'title', 'address', 'guapai', 'chengjiao','fang', 'lou', 'dealdate')
    chengjiao_list = tablib.Dataset(*chengjiao_list, headers=headers)

    with open('D:\chengjiao_' + EXCEL_NAME + current_time + '.xlsx', 'wb') as f:
        f.write(chengjiao_list.export('xlsx'))


if __name__ == "__main__":
    main()
