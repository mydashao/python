#
# 1. 扫码登录
# 2. 记录cookie
# 3. 再次登录读取cookie
# 4. 自动领券
# 5. 记录购物车
# 6. 记录优惠券

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

# 常量，阅读观看等时长，单位分钟

url_list = ('',
            '',
            '',
            '',
            '',
            '',)

starttime = datetime.datetime.now()

COOKIE_FILE='D:\JD_cookie.txt'

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
file_handler = logging.FileHandler('D:\qg.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def main():
    logger.info('程序开始运行!')
    login()

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
    logger.debug('     开始保存cookie')
    time.sleep(1)
    with open(COOKIE_FILE, 'w') as f:
        f.write(str(cookies))
    logger.debug('     保存cookie成功')
    time.sleep(1)


# 获取程序保存在COOKIE_FILE中的cookie
def get_cookie():
    logger.debug('     开始读取cookie')
    time.sleep(1)
    with open(COOKIE_FILE, 'r') as f:
        cookies= f.read()
        cookie_list = eval(cookies)
        logger.debug('     读取cookie成功')
        print(cookie_list)
        time.sleep(1)
        return cookie_list

def if_time(start,end):
    flag = 0
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + start, '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + end, '%Y-%m-%d%H:%M')
    n_time = datetime.datetime.now()
    if n_time < start_time:
        flag = -1
    elif n_time >= start_time and n_time < end_time:
        flag = 0
    else:
        flag = 1

    return flag

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
        time.sleep(3)
    except FileNotFoundError:
        logger.debug('     cookie文件未找到')

    # 如cookie过期，扫码登陆，如果出现提示框，关闭然后跳转到扫码界面

    # 向下移动700 方便扫码
    js = "document.documentElement.scrollTop=700"
    browser.execute_script(js)

    # 显示等待，如title= “我的积分”，则结束倒计时，进行下一步
    logger.debug('     请在60秒内扫码')
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
    get_ticket(browser)

def get_ticket(browser):


    # count记录刷新次数， 每部分完成，end+1，五个部分结束 end=5 score记录总得分。
    while 1==1:
        begin = '20:32'
        end = '20:35'
        if if_time(begin,end) ==0:
            print('时间到了')
            refresh(browser)

        elif if_time(begin,end) ==-1:
            print('时间未到')
            time.sleep(40)

        elif if_time(begin,end) ==1:
            print('时间过了')
            break

    logger.info('任务完成！！！')
    time.sleep(1)
    # logging.info('今天完成',score,'分，耗时',min,'分',sec,'秒')
    logger.info('今天完成 %d 分，耗时 %d 分 %d 秒')
    logger.info('===============================')

def refresh(browser):
    print('refresh')
    browser.execute_script('window.open()')
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])
    time.sleep(5)

    browser.get('https://item.jd.com/100002720639.html')
    time.sleep(5)
    for i in range(6000):
        browser.refresh()
        print('refresh',i)
        time.sleep(10)




# 主方法,如果变量__name__为主方法，执行下一步，
# 如果被其他程序引用，变量__name__为本文件名（xxqg），！=__main__，不继续进行
if __name__ == "__main__":
    main()


