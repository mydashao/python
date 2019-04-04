
# 获取视频长度，
# 根据当前时间，确定学习时长
# 文章获得焦点
# 视频音量最小化
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
cookie="cookie: __UID__=181dac50-492b-11e9-a898-5ba8c5112414; token=ea004323ae634ed698d68f5b021da2d0"

# 常量，阅读观看等时长，单位分钟
READ=2
WATCH = 2
READ_TIME = 5
WATCH_TIME = 5
LOGIN_MSG='每日首次登录+1分'
READ_MSG='阅读一篇文章+1分'
WATCH_MSG='观看一个视频+1分'
READ_TIME_MSG='有效阅读文章累计2分钟+1分'
WATCH_TIME_MSG='有效观看视频累计3分钟+1分'
COMPLETE_MSG='已完成'
starttime = datetime.datetime.now()
COOKIE_FILE='D:\cookie.txt'
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
    get_session()

def get_time(sec):
    timeArray = time.localtime(sec)  # 1970秒数
    cookie_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    rest_hour = (sec - time.time()) // 3600
    rest_minute = (sec - time.time()) % 3600 // 60
    logger.debug('     cookie当前时间：%s',current_time)
    time.sleep(1)
    logger.debug('     cookie过期时间：%s',cookie_time)
    time.sleep(1)
    # logger.debug('      距离cookie过期还剩',rest_hour,'小时',rest_minute,'分')


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
        time.sleep(1)
        return cookie_list

def get_session():
    # 打开积分页面
    login_url = 'https://pc.xuexi.cn/points/my-points.html'
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
        WebDriverWait(browser, 60, 0.5).until(EC.title_is('我的积分'))
    except:
        logger.debug('     没有人扫码啊，我走了')
        browser.quit()
        return

    # 保存cookie
    cookies = browser.get_cookies()
    # logger.debug('      这个是最新的cookies',cookies)
    save_cookie(cookies)

    # 得到cookie中token的过期时间，判断还有几个小时过期
    for cookie in cookies:
        if cookie.get('name') == 'token':
            get_time(cookie.get('expiry'))

    # count记录刷新次数， 每部分完成，end+1，五个部分结束 end=5 score记录总得分。
    end = 0
    count = 0
    while end != 5:
        end = 0
        score = 0
        count = count+1

        logger.debug('     刷新后计算 %s 次',count)
        browser.refresh()
        time.sleep(3)

        # detail为得分情况文字,
        # complete为按钮中是否完成文字,
        # had为每部分已得到的分数
        buttons = browser.find_elements_by_class_name('my-points-card')
        for button in buttons:
            detail = button.find_element_by_class_name('my-points-card-subtitle').text
            complete = button.find_element_by_class_name('buttonbox').text
            had = int(button.find_element_by_class_name('my-points-card-text').text.split("/")[0][0:-1])
            # rest = 0
            score = score + had

            # logger.debug('         '+detail+'-------'+complete,had,'-------',score)
            logger.debug('         %s ---%s：%s---今日总分：%d',detail,complete,had,score)

            # 每阶段如已完成，end+1
            # 如尚未完成,输出还剩多少分,并转到响应方法执行学习功能
            if detail == LOGIN_MSG :
                time.sleep(1)
                if complete == COMPLETE_MSG:
                    end = end+1

                else :logger.debug('请登录')

            elif detail == READ_MSG :
                time.sleep(1)
                if  complete == COMPLETE_MSG:
                    # logger.debug('阅读完成')
                    end = end+1

                else:
                    rest = 6-had
                    logger.debug('         阅读剩余分数:%d分',rest)
                    js='https://www.xuexi.cn/3695ce40a2f38ca24261ee28953ce822/data9a3668c13f6e303932b5e0e100fc248b.js'
                    study(browser,1,js,rest)
                    break

            elif detail == WATCH_MSG:
                time.sleep(1)
                if complete == COMPLETE_MSG:
                    # logger.debug('观看完成')
                    end = end+1

                else:
                    rest = 6-had
                    logger.debug('         视频剩余分数:%d分',rest)
                    js = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/datab87d700beee2c44826a9202c75d18c85.js'
                    study(browser,2,js,rest)
                    break

            elif detail == READ_TIME_MSG:
                time.sleep(1)
                if complete == COMPLETE_MSG:
                    # logger.debug('阅读时间完成')
                    end = end+1

                else:
                    rest = 6 - had
                    logger.debug('         阅读学习时长剩余分数:%d分', rest)
                    js = 'https://www.xuexi.cn/3695ce40a2f38ca24261ee28953ce822/data9a3668c13f6e303932b5e0e100fc248b.js'
                    study(browser,3,js,rest)
                    break

            elif detail == WATCH_TIME_MSG:
                time.sleep(1)
                if complete == COMPLETE_MSG:
                    # logger.debug('观看时间完成')
                    end = end+1
                else:
                    rest = 6 - had
                    logger.debug('         视频学习时长剩余分数:%d分', rest)
                    js ='https://www.xuexi.cn/9b202c09ea962c54c625cdd0e272bd2a/data577a3dee30fbeb9ab03295a860c2a295.js'
                    study(browser,4,js,rest)
                    break

    endtime = datetime.datetime.now()
    secmin = (endtime - starttime).seconds
    min = secmin // 60
    sec = secmin % 60
    time.sleep(1)
    logger.info('任务完成！！！')
    time.sleep(1)
    # logging.info('今天完成',score,'分，耗时',min,'分',sec,'秒')
    logger.info('今天完成 %d 分，耗时 %d 分 %d 秒',score,min,sec)
    logger.info('===============================')

def study(browser,type,js,rest):
    part=['阅读文章','观看视频','文章学习时长','视频学习时长']
    logger.debug('         开始%s学习:', part[type-1])
    res = requests.get(js)
    res.encoding = 'utf-8'
    url_list = []
    # 根据列表js,解析文章url，添加到列表
    for key, value in json.loads(res.text.lstrip('globalCache = ').rstrip(';'), encoding="utf-8").items():
        if key != 'sysQuery':
            for item in value['list']:
                url_list.append(item['static_page_url'])
            # 从列表中随机选取一个url打开
            size = len(url_list)
            url = url_list[int(random.randint(1, size - 1))]
            logger.debug('         '+url)

            if type == 1 :           time = 2
            elif type==  2 :         time = 3
            elif type == 3:          time = rest*2
            else:time = rest*3

            read_watch(browser, url, time, type)

# 阅读或观看的方法
def read_watch(browser,url,times,type):

    # 新建页面，新建句柄，切换句柄到新建页面，新页面打开url
    browser.execute_script('window.open()')
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])
    browser.get(url)
    time.sleep(2)
    # 获得动作链，为在页面获得焦点，执行tab按键
    action = ActionChains(browser)
    action.send_keys(Keys.TAB)
    action.perform()
    # 奇数是文章，偶数是视频，如果是视频，得到视频标签
    if (type % 2) == 0:
        video = browser.find_element_by_tag_name("video")
        # duration = browser.find_element_by_class_name("duration")
        # url = browser.execute_script("return arguments[0].currentSrc;", video)
        # 播放视频
        browser.execute_script("return arguments[0].play()", video)
    # 根据传递的学习时长学习

    total_time = times*63
    for i in range(total_time):
        print('\r' ,'                              学习剩余时长：', str(total_time - i-1),'/',total_time,'秒', end='', flush=True)

        time.sleep(1)

        # 每分钟向下移动滚动条，模仿阅读
        if i % 20 == 0:
            js = "document.documentElement.scrollTop=" + str(i*3)
            browser.execute_script(js)

    print('')

    # 关闭学习页面，切换句柄到积分目录
    time.sleep(2)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(handles[0])

# 主方法,如果变量__name__为主方法，执行下一步，
# 如果被其他程序引用，变量__name__为本文件名（xxqg），！=__main__，不继续进行
if __name__ == "__main__":
    main()


