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

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
# 将日志消息发送到输出到Stream，如std.out, std.err或任何file-like对象。
console_handler = logging.StreamHandler(sys.stderr)
# 设置handler将会处理的日志消息的最低严重级别
console_handler.setLevel(logging.DEBUG)
# 设置消息格式，日期格式等
format = logging.Formatter(fmt="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(format)

# 将日志消息发送到磁盘文件，默认情况下文件大小会无限增长
file_handler = logging.FileHandler('D:\JD\qg.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
ticket_url = "https://quan.jd.com/user_quan.action"

def main():
    logger.info('=============================================')
    logger.info('程序开始运行!')
    browser = login()
    # 导出优惠券
    # ticket_list(browser,ticket_url)
    # 刷优惠券
    ticket(browser)
    # 导出订单
    # ?order_list(browser)
    # ticket_old(browser)


def get_time(sec):
    timeArray = time.localtime(sec)  # 1970秒数
    cookie_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    rest_hour = (sec - time.time()) // 3600
    rest_minute = (sec - time.time()) % 3600 // 60
    logger.debug('     cookie当前时间：%s',current_time)
    time.sleep(1)
    logger.debug('     cookie过期时间：%s',cookie_time)
    time.sleep(1)
    logger.debug('      距离cookie过期还剩',rest_hour,'小时',rest_minute,'分')

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
        logger.debug('     没有人扫码啊，我走了')
        browser.quit()
        return

    # 保存cookie
    cookies = browser.get_cookies()
    # logger.debug('      这个是最新的cookies',cookies)
    save_cookie(cookies)
    return browser



def ticket_old(browser):
    threads = []
    begin_list = [1, 2, 3, 4, 5, 6, 7]

    for i in range(len(begin_list)):
        threads.append(threading.Thread(target=refresh_old, args=(browser,begin_list[i])))

    for t in threads:
        # t.setDaemon(True)
        t.start()


def refresh_old(browser,chrome):
    # browser = webdriver.Chrome()

    for i in range(4):
        browser.execute_script('window.open()')
        print(chrome,'打开第',i+1,'个页面')
        time.sleep(1)

    handles = browser.window_handles
    url = 'https://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=265db24ca1534198aa79c68b4aa15721&roleId=20316886&to=//mall.jd.com/index-1000132921.html'
    for times in range(100):
        for j in range(len(handles)):
            browser.switch_to.window(handles[j])
            browser.get(url)
            print(str(datetime.datetime.now())[:-3],'第',chrome,'个浏览器打开第',j+1,'个页面刷新第',times+1, '次')
            time.sleep(1)



def ticket(browser):
    u1 = "https://pro.jd.com/mall/active/368byKmXwznBuAzB59dUKsPsqpcY/index.html?extension_id=eyJhZCI6IiIsImNoIjoiIiwic2hvcCI6IiIsInNrdSI6IiIsInRzIjoiIiwidW5pcWlkIjoie1wiY2xpY2tfaWRcIjpcIjM5MTk3OTE2LTU0MDYtNDBkOS1iZGQ1LTVmNjVjY2EwNDNiMlwiLFwibWF0ZXJpYWxfaWRcIjpcIjQ5MDgyNzEzNVwiLFwicG9zX2lkXCI6XCI0Mjc1XCIsXCJzaWRcIjpcImZhNTczZTJjLWZiYzYtNDNhNy05ZGQ1LWIwMmNmMWUwMzI0ZFwifSJ9&jd_pop=39197916-5406-40d9-bdd5-5f65cca043b2&abt=1"
    url3 = "https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&body=%7B%22activityId%22%3A%22nKxVyPnuLwAsQSTfidZ9z4RKVZy%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3D0D46D6216C47799812D08243016C30A6F3B829B8055491ACC879AE44A78994C67E71EC00BE56F9C1BE40AD949D1C6C83_babel%2CroleId%3D3EF119C217F04E550F41047BEB79C3FD_babel%22%2C%22eid%22%3A%226HTBRM32KJCEPPYHNWWOWM47S3MZKRGILSHHCFTRGIHISGF5VKP3O6NXUKPJF76VV2CCRQ2SFE6B3C7DREQ7QSGJ4U%22%2C%22fp%22%3A%22edc3faef203541bcff5d9afa30e5873e%22%2C%22pageClick%22%3A%22Babel_Coupon%22%2C%22mitemAddrId%22%3A%22%22%2C%22geo%22%3A%7B%22lng%22%3A%22%22%2C%22lat%22%3A%22%22%7D%7D&screen=750*1334&client=wh5&clientVersion=1.0.0&sid=&uuid=&area=&loginType=3&callback=jsonp4"
    url1 = "https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&body=%7B%22activityId%22%3A%223w3DzbkB5ncd1pgQAuV6oDKpYM9B%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3D67C6E14317527492F6235FC20792D97F5CBE483A7A52E447194EBFBE839552BB04B8F07643AF3FA58C4611FE38FB72E3_babel%2CroleId%3DD6B31BB81863ECC45BC2D7F30420AD29_babel%22%2C%22eid%22%3A%226HTBRM32KJCEPPYHNWWOWM47S3MZKRGILSHHCFTRGIHISGF5VKP3O6NXUKPJF76VV2CCRQ2SFE6B3C7DREQ7QSGJ4U%22%2C%22fp%22%3A%22edc3faef203541bcff5d9afa30e5873e%22%2C%22pageClick%22%3A%22Babel_Coupon%22%2C%22mitemAddrId%22%3A%22%22%2C%22geo%22%3A%7B%22lng%22%3A%22%22%2C%22lat%22%3A%22%22%7D%7D&screen=750*1334&client=wh5&clientVersion=1.0.0&sid=&uuid=&area=&loginType=3&callback=jsonp3"
    url3 = "https://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=265db24ca1534198aa79c68b4aa15721&roleId=20316886&to=//mall.jd.com/index-1000132921.html"
    url4 = "https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&body=%7B%22activityId%22%3A%22378jVWoR2PmtVp9gtXAGySL82YTy%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3D4FAF8BA685D85534EC53A86A83B734D4F2801639C53FB1B3095F12EF7F6BD9B5F320BAC296C1506B3F80B14F8CF40B83_babel%2CroleId%3D009D524844052C3B4A455FA36AD70673_babel%22%2C%22eid%22%3A%22SPKSYS2J4DUUCUAKKN63BR5RIIPPMJU6S6TQBJEOI7BBCJRPUTZDW5HNYB3JAQUL3P2QAXKP6JJ6F5SZ7SQUAISINQ%22%2C%22fp%22%3A%22d844de2da4d30435798ce566949038cc%22%2C%22pageClick%22%3A%22Babel_Coupon%22%2C%22mitemAddrId%22%3A%22%22%2C%22geo%22%3A%7B%22lng%22%3A%22%22%2C%22lat%22%3A%22%22%7D%7D&screen=750*1334&client=wh5&clientVersion=1.0.0&sid=&uuid=&area=&loginType=3&callback=jsonp4"
    url5 = "https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&body=%7B%22activityId%22%3A%22378jVWoR2PmtVp9gtXAGySL82YTy%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3D4FAF8BA685D85534EC53A86A83B734D4F2801639C53FB1B3095F12EF7F6BD9B5F320BAC296C1506B3F80B14F8CF40B83_babel%2CroleId%3D009D524844052C3B4A455FA36AD70673_babel%22%2C%22eid%22%3A%22SPKSYS2J4DUUCUAKKN63BR5RIIPPMJU6S6TQBJEOI7BBCJRPUTZDW5HNYB3JAQUL3P2QAXKP6JJ6F5SZ7SQUAISINQ%22%2C%22fp%22%3A%22d844de2da4d30435798ce566949038cc%22%2C%22pageClick%22%3A%22Babel_Coupon%22%2C%22mitemAddrId%22%3A%22%22%2C%22geo%22%3A%7B%22lng%22%3A%22%22%2C%22lat%22%3A%22%22%7D%7D&screen=750*1334&client=wh5&clientVersion=1.0.0&sid=&uuid=&area=&loginType=3&callback=jsonp4"

    begin_list = ["23:58:47", "23:58:47", "23:58:43", "23:58:41",
                  "23:58:47", "23:58:47", "23:58:43", "23:58:41",
                  "23:58:47", "23:58:47", "23:58:43", "23:58:41",
                  "23:58:47", "23:58:47", "23:58:43", "23:58:41"]

    # begin_list = ["23:59:10", "23:59:45", "23:59:43", "23:59:39", "23:59:36", "23:59:40", "23:59:47"]
    name_list = ["1【888-666网络】", "2【888-666网络】", "3【888-666网络】", "4【888-666网络】",
                 "5【888-666网络】", "6【888-666网络】", "7【888-666网络】", "8【618-300手表】",
                 "9【199-100外设】", "10【199-100外设】", "11【199-100外设】", "12【199-100外设】",
                 "13【618-300手表】", "14【199-100外设】", "15【618-300手表】", "16【199-100外设】"]
    url_list = [url1, url1, url1, url1, url1, url1, url1,url1,
                url1, url1, url1, url1, url1, url1, url1, url1]
    color = ['33', '32', '36', '34', '35', '37', '31',
             '33', '32', '36', '34', '35', '37', '31',
             '33', '32']

    # get_ticket(browser,begin_list,name_list,url_list)

    threads = []
    lock = threading.Lock()

    for i in range(len(begin_list)):
        threads.append(
            threading.Thread(target=get_ticket, args=(browser, begin_list[i], name_list[i], url_list[i], color[i],lock)))

    for t in threads:
        # t.setDaemon(True)
        t.start()
        time.sleep(1.27)

def get_ticket(browser,begin,name,url,color,lock):

    start_line = '\033[1;' + color + 'm '
    end_line = '\033[0m'

    END = 0
    while END!=1:

        sec = if_time(begin)
        if sec<-100 and sec>-85800:
            print(start_line,str(datetime.datetime.now())[:-3],name, '时间未到，还差', -1 * sec, '秒',end_line)
            time.sleep(min(-1 * sec / 2, 900))

        elif -100<=sec <0:
            for j in range (-1*sec-30):
                print(start_line,str(datetime.datetime.now())[:-3],name,'时间未到，还差',-1*sec-j,'秒',end_line)
                time.sleep(1)
            END = refresh(browser, name, url,color,lock)

        elif (sec >= 0 and sec <= 300) or sec<=-85800 :

            print(start_line,str(datetime.datetime.now())[:-3],name,'时间过了',sec,'秒',end_line)
            END= refresh(browser, name, url,color,lock)

        elif sec >300:

            print(start_line,str(datetime.datetime.now())[:-3],name,'超过五分钟了,退出',end_line)
            END = 1
            # break


def refresh(browser,name,url,color,lock):
    start_line = '\033[1;' + color + 'm '
    end_line = '\033[0m'
    browser.execute_script('window.open()')
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])
    browser.get(url)
    for i in range(1000):
            lock.acquire()
            browser.get(url)
            print(" ",str(datetime.datetime.now())[:-3],name,'刷新',i,'次')
            try:
                info_raw = browser.find_element_by_tag_name('pre').text
            except:
                browser.refresh()
                try:
                    info_raw = browser.find_element_by_tag_name('pre').text
                except:
                    info_raw = 'jsonp5({"subCodeMsg":"重复~~很抱歉，没抢到~~","subCode":"A28","code":"0","msg":null})'

            info_format = info_raw[info_raw.find("{"):-1].replace('null', '"null"')
            lock.release()

            try:
                msg_list = eval(info_format)
                msg = msg_list.get('subCodeMsg')
            except:
                msg = info_raw
            try:
                code = msg_list.get('subCode')
            except:
                code = "A00"

            if code == "A28" :
                print(name+"：很抱歉，没抢到~~")
            elif code == "A14":
                logger.info(name+"：此券今日已经被抢完，请您明日再来~")
                # return 1
                # break
            elif code == "A15" :
                logger.info(name+"：此券已经被抢完了，下次记得早点来哟~")
                return 1
                break

            elif code == "A13":
                logger.info(name+"：您今天已经参加过此活动，别太贪心哟，明天再来~")
                return 1
                break
            elif code == "A6":
                logger.info(name + "：您来太晚了，活动已经结束了哟~")
                return 1
                break
            elif code == "A12":
                logger.info(name + "：您已经参加过此活动，别太贪心哟，下次再来~")
                return 1
                break
            elif code =='D2':
                logger.info(name + "：本时段优惠券已抢完，请14:00再来吧！")

            elif code == "A1":
                logger.info(name + "：领取成功！感谢您的参与，祝您购物愉快~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                return 1
                break
            else:
                print(" ",str(datetime.datetime.now())[:-3], name,code, msg)
            # time.sleep

# 爬取用户优惠券信息
def ticket_list(browser,url):
    browser.get(url)
    list = browser.find_elements_by_class_name('coupon-item-d')
    for item in list:
        ticket_type =item.find_element_by_class_name('c-type').find_element_by_class_name('c-price').find_element_by_class_name('type').text.strip()
        price = item.find_element_by_class_name('c-type').find_element_by_class_name('c-price').find_element_by_tag_name('strong').text.strip()
        limit = item.find_element_by_class_name('c-type').find_element_by_class_name('c-limit').text.strip()[1:-2]
        use_time = item.find_element_by_class_name('c-type').find_element_by_class_name('c-time').text.strip()
        tips = item.find_element_by_class_name('c-msg').find_element_by_class_name('c-range').find_element_by_class_name('range-item').find_element_by_class_name('txt').text.strip()
        # use_time = item.find_element_by_class_name('c-msg').find_element_by_class_name('c-range').find_element_by_class_name('range-item').find_element_by_class_name('txt').text.strip()
        lenth = 30-len(tips)
        space = ''
        for i in range(lenth):
            space =space+' '
        print(ticket_type,'-',tips,space,limit,'-',price)
    try:
        next = browser.find_element_by_class_name('ui-page-wrap').find_element_by_class_name('ui-page').find_element_by_class_name('ui-pager-next').text[0:3]
        # print(next)
        if next =='下一页':
            next_page =browser.find_element_by_class_name('ui-page-wrap').find_element_by_class_name('ui-page').find_element_by_class_name('ui-pager-next').get_attribute('href')
            # next_page = "https://quan.jd.com/"+next_page
            # print(next_page)
            ticket_list(browser,next_page)
    except:
        print("没有了")
        return
# def shopping_cart():
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
                    for i in range(good_number):
                        order_name = order_goods[i].text
                        order_number = order_numbers[i].text[1:]



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