#
# 1. 扫码登录
# 2. 记录cookie
# 3. 再次登录读取cookie
# 4. 自动领券
# 5. 记录购物车
# 6. 记录优惠券
import tablib

import sys
import logging
import datetime
import json
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading

# 常量，阅读观看等时长，单位分钟

mylist=[]
starttime = datetime.datetime.now()

COOKIE_FILE='D:\JD\JD_cookie.txt'

current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

LOG_FORMAT = "%(asctime)s- %(message)s"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S "

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


def main():
    print('=============================================')
    print('程序开始运行!')
    browser = login()
    order_list(browser)



# 保存扫码后的cookie在COOKIE_FILE
def save_cookie(cookies):
    print(' ', str(datetime.datetime.now())[:-3], '开始保存cookie')
    time.sleep(0.5)
    with open(COOKIE_FILE, 'w') as f:
        f.write(str(cookies))
        print(' ', str(datetime.datetime.now())[:-3], '保存cookie成功')
    time.sleep(0.5)


# 获取程序保存在COOKIE_FILE中的cookie
def get_cookie():
    print(' ', str(datetime.datetime.now())[:-3],'开始读取cookie')
    time.sleep(1)
    with open(COOKIE_FILE, 'r') as f:
        cookies= f.read()
        cookie_list = eval(cookies)
        print(' ', str(datetime.datetime.now())[:-3], '读取cookie成功')
        # print(cookie_list)
        time.sleep(1)
        return cookie_list

def if_time(start):
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + start, '%Y-%m-%d%H:%M:%S')
    # end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + end, '%Y-%m-%d%H:%M')
    current_time = datetime.datetime.now()

    interval = current_time - start_time
    sec = interval.days * 24 * 3600 + interval.seconds
    return sec

def login():
    # 打开领券页面
    login_url = 'https://order.jd.com/center/list.action'
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(login_url)

    # 获得已保存的cookie
    try:
        cookies = get_cookie()
        # logger.debug('      这个是读取的cookies', cookies)
        for cookie in cookies:
            browser.add_cookie(cookie)
        # 利用已保存的cookie访问积分页面
        browser.get(login_url)
        # time.sleep(1)
    except :
        print(' ',str(datetime.datetime.now())[:-3],'cookie文件未找到')
        print(' ',str(datetime.datetime.now())[:-3],'请在60秒内扫码')

    # 如cookie过期，扫码登陆，如果出现提示框，关闭然后跳转到扫码界面


    # 显示等待，如title= “我的积分”，则结束倒计时，进行下一步
    try:
        WebDriverWait(browser, 60, 0.5).until(EC.title_is('我的京东--我的订单'))
    except:
        print('     没有人扫码啊，我走了')
        browser.quit()
        return

    # 保存cookie
    cookies = browser.get_cookies()
    # logger.debug('      这个是最新的cookies',cookies)
    save_cookie(cookies)
    return browser


def order_list(browser):
    year_list=['2019','2018','2017','2016','2015','2014','3']

    front_url = 'https://order.jd.com/center/list.action?search=0&d='
    last_url = '&s=4096&page='
    browser.execute_script('window.open()')
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])

    for i in range(len(year_list)):
        page_number = 0

        # url = front_url + year_list[i] + last_url + str(page_number)
        # browser.get(url)
        # time.sleep(1)
        # print(browser.page_source)
        next_page = '下一页'

        while next_page =='下一页':
            page_number = page_number + 1

            url = front_url+year_list[i]+last_url+str(page_number)

            print(url)
            browser.get(url)
            # print(browser.page_source)
            time.sleep(1)

            list = browser.find_elements_by_tag_name("tbody")
            for item in list:
                order_time = item.find_element_by_class_name('dealtime').text
                try:
                    order_status = item.find_element_by_class_name('order-status').text
                except:
                    order_status=''
                order_id = item.find_element_by_class_name('number').find_element_by_tag_name('a').text

                try:
                    order_type= item.find_element_by_class_name('number').find_element_by_tag_name('a').get_attribute('name')
                except:
                    order_type = item.find_element_by_class_name('number').find_element_by_tag_name('a').get_attribute('href')
                if order_type =='orderIdLinks':
                    # 一个多商品订单中，有多个商品名称和商品数量
                    order_goods =  item.find_elements_by_class_name('p-name')
                    order_numbers =  item.find_elements_by_class_name('goods-number')

                    order_price = item.find_element_by_class_name('amount').find_element_by_tag_name('span').text[4:]
                    order_pay = item.find_element_by_class_name('amount').find_element_by_class_name('ftx-13').text
                    # order_address = item.find_element_by_class_name('consignee').find_element_by_class_name('prompt-01').find_element_by_class_name('pc').find_element_by_tag_name('p').text.strip()
                    order_consignee = item.find_element_by_class_name('consignee').text
                    good_number = len(order_goods)
                    for k in range(good_number):
                        order_name = order_goods[k].text
                        order_number = order_numbers[k].text[1:]



                    # for order_good in order_goods:
                    #     order_name = order_good.text
                        # 订单单件商品
                        if good_number>0:
                                print( order_time,order_id,order_name,order_number,order_price,order_consignee,order_pay, order_status)
                                mylist.append([order_id, order_name,  order_number, order_price,
                                               order_consignee,order_time,order_pay, order_status])
                        # 订单多件商品
                        else :
                            print( order_time,order_id,  order_name, order_number, ' ', ' ',' ', ' ')
                            mylist.append(['', order_name, order_number,' ', ' ',' ', ' ', order_status])
                        good_number = good_number -10
                # 拆分订单
                else:
                    order_time = item.find_element_by_class_name('dealtime').text
                    last_order_time = order_time
                    try:
                        order_status = item.find_element_by_class_name('order-status').text[5:]
                    except:
                        order_status = ''
                    order_separate = item.find_element_by_class_name('ftx-13').text
                    order_pay =  item.find_element_by_class_name('order-pay').text[6:]
                    order_consignee = item.find_element_by_class_name('order-consignee').text[4:]
                    order_price =  item.find_element_by_class_name('order-count').text[6:]
                    print(order_time,order_id, order_separate,'1',order_price,order_consignee,order_pay,order_status)

                    if order_time == last_order_time:
                        mylist.append([order_id, order_separate, '1', order_price,
                                       order_consignee, order_time, order_pay, order_status])
                    else :
                        mylist.append([order_id, order_separate,'1',order_price,
                                   order_consignee,order_time,order_pay,order_status])

                try:
                    next_page = browser.find_element_by_class_name("mt20").find_element_by_class_name(
                        "pagin").find_element_by_xpath('//a[@class="next"]').text

                except:
                    # next_page = browser.find_element_by_class_name("mt20").find_element_by_class_name("pagin").find_element_by_tag_name('next-disabled').text
                    next_page = 'disable'
            headers = (
                '订单编号', '商品', '数量', '总价', '收货人', '时间', '付款方式', '状态')
            dict = 'D:\JD\order_list_'
            save_to_excel(headers, mylist, dict)



def save_to_excel(headers,mylist,dict):


    #print(mylist)
    mylist = tablib.Dataset(*mylist, headers=headers)

    with open(dict+'.xlsx', 'wb') as f:
        f.write(mylist.export('xlsx'))

# 主方法,如果变量__name__为主方法，执行下一步，
# 如果被其他程序引用，变量__name__为本文件名（xxqg），！=__main__，不继续进行
if __name__ == "__main__":
    main()