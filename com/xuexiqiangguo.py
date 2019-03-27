
# 获取视频长度，
# 根据当前时间，确定学习时长
# 文章获得焦点
# 视频音量最小化


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
READ=2
WATCH = 2
READ_TIME = 5
WATCH_TIME = 5

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

# 调用cookie方法，尚未完成
def use_cookie():
    get_session()

def get_session():

    login_url = 'https://pc.xuexi.cn/points/my-points.html'

    browser = webdriver.Chrome()
    browser.get(login_url)

    # 显示等待，如title= “我的积分”，则结束倒计时，进行下一步
    print('请在60秒内扫码')

    try:
        WebDriverWait(browser, 60, 0.5).until(EC.title_is('我的积分'))
    except:
        print("没有人扫码啊，我走了")
        browser.quit()
        return

    # count记录刷新次数， 每部分完成，end+1，五个部分结束 end=5 score记录总得分。
    end = 0
    count = 0
    while end != 5:
        end = 0
        score = 0
        count = count+1

        print('刷新后计算',count,'次')
        time.sleep(2)
        browser.refresh()
        time.sleep(3)

        # detail为得分情况文字,
        # complete为按钮中是否完成文字,
        # had为每部分已得到的分数
        buttons = browser.find_elements_by_class_name('my-points-card')
        for button in buttons:
            detail = button.find_element_by_class_name('my-points-card-subtitle').text
            complete = button.find_element_by_class_name('buttonbox').text
            had = button.find_element_by_class_name('my-points-card-text').text.split("/")[0][0:-1]
            # rest = 0
            score = score + int(had)

            print(detail+'-------'+complete,had,'-------',score)

            # 每阶段如已完成，end+1
            # 如尚未完成,输出还剩多少分,并转到响应方法执行学习功能
            if detail == '每日首次登录+1分' :
                time.sleep(1)
                if complete == '已完成':
                    end = end+1
                else :print('请登录')

            elif detail == '阅读一篇文章+1分' :
                time.sleep(1)
                if  complete == '已完成':
                    # print('阅读完成')
                    end = end+1
                else:
                    print('阅读还剩:'+str(6-int(had))+'分')
                    read(browser,had)
                    break

            elif detail == '观看一个视频+1分':
                time.sleep(1)
                if complete == '已完成':
                    # print('观看完成')
                    end = end+1
                else:
                    print('视频还剩:'+str(6-int(had))+'分')
                    watch(browser,had)
                    break

            elif detail == '阅读文章每累计4分钟+1分' :
                time.sleep(1)
                if complete == '已完成':
                    # print('阅读时间完成')
                    end = end+1
                else:
                    print('阅读学习时长还剩:'+str(8-int(had))+'分')
                    readtime(browser,had)
                    break

            elif detail == '观看视频每累计5分钟+1分' :
                time.sleep(1)
                if complete == '已完成':
                    # print('观看时间完成')
                    end = end+1
                else:
                    print('视频学习时长还剩:'+str(10-int(had))+'分')
                    watchtime(browser,had)
                    break

    print('-----任务完成！！！-----总计',score,'分-----')

# 阅读文章方法
def read(browser,rest):
    print('开始阅读学习')
    type = 'text'
    # 从浏览器请求得到记录文章列表的js
    js = 'https://www.xuexi.cn/3695ce40a2f38ca24261ee28953ce822/data9a3668c13f6e303932b5e0e100fc248b.js'
    res = requests.get(js)
    res.encoding = 'utf-8'
    # print(res.text)
    url_list = []
    # 根据列表js,解析文章url，添加到列表
    for key, value in json.loads(res.text.lstrip('globalCache = ').rstrip(';'), encoding="utf-8").items():
        if key != 'sysQuery':
            for item in value['list']:
                url_list.append(item['static_page_url'])
            # 从列表中随机选取一个url打开
            size = len(url_list)
            url = url_list[int(random.randint(1, size - 1))]
            print(url)
            read_watch(browser, url, READ,type)


def watch(browser,rest):
    print('开始视频学习')
    type = 'video'
    js = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/datab87d700beee2c44826a9202c75d18c85.js'
    res = requests.get(js)
    res.encoding = 'utf-8'
    # print(res.text)
    url_list = []
    for key, value in json.loads(res.text.lstrip('globalCache = ').rstrip(';'), encoding="utf-8").items():
        if key != 'sysQuery':
            for item in value['list']:
                # print(item['static_page_url'], item['frst_name'], item['original_time'])
                url_list.append(item['static_page_url'])
            size = len(url_list)
            url = url_list[int(random.randint(1,size-1))]
            print(url)
            read_watch(browser, url, WATCH,type)


def readtime(browser,rest):
    print('开始阅读学习时长')
    type = 'text'
    js = 'https://www.xuexi.cn/3695ce40a2f38ca24261ee28953ce822/data9a3668c13f6e303932b5e0e100fc248b.js'
    res = requests.get(js)
    res.encoding = 'utf-8'
    # print(res.text)
    url_list = []
    for key, value in json.loads(res.text.lstrip('globalCache = ').rstrip(';'), encoding="utf-8").items():
        if key != 'sysQuery':
            for item in value['list']:
                url_list.append(item['static_page_url'])
            size = len(url_list)
            url = url_list[int(random.randint(1, size - 1))]
            print(url)
            read_watch(browser,url, READ_TIME,type)

def watchtime(browser,had):
    print('开始视频学习时长')
    type = 'video'
    rest = 10-int(had)
    js = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/datab87d700beee2c44826a9202c75d18c85.js'
    xwlb = 'https://www.xuexi.cn/9b202c09ea962c54c625cdd0e272bd2a/data577a3dee30fbeb9ab03295a860c2a295.js'
    res = requests.get(xwlb)
    res.encoding = 'utf-8'
    # print(res.text)
    url_list = []
    for key, value in json.loads(res.text.lstrip('globalCache = ').rstrip(';'), encoding="utf-8").items():
        if key != 'sysQuery':
            for item in value['list']:
                # print(item['static_page_url'], item['frst_name'], item['original_time'])
                url_list.append(item['static_page_url'])
            size = len(url_list)
            url = url_list[int(random.randint(1, size - 1))]
            print(url)
            # 观看时长重写为剩余分数*5分钟，保险起见加一分钟，一次性看完
            WATCH_TIME= rest*5+1
            read_watch(browser,url,WATCH_TIME,type)


# 阅读或观看的方法
def read_watch(browser,url,times,type):
    # times = int(times/2)+1

    # 新建页面，新建句柄，切换句柄到新建页面，新页面打开url
    browser.execute_script('window.open()')
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])
    browser.get(url)
    # 如果是视频，得到视频标签
    if type =='video':
        video = browser.find_element_by_tag_name("video")
        # duration = browser.find_element_by_class_name("duration")
        # url = browser.execute_script("return arguments[0].currentSrc;", video)
        time.sleep(2)
        # 获得动作链，为在页面获得焦点，执行tab按键
        action = ActionChains(browser)
        action.send_keys(Keys.TAB)
        action.perform()
        # 播放视频
        print("开始播放视频，总长：")
        browser.execute_script("return arguments[0].play()", video)
    # 根据传递的学习时长学习
    for i in range(times):
        print('学习还剩'+str(times-i)+'分  ', end="")
        # 每分钟向下移动滚动条70像素，模仿阅读
        js = "document.documentElement.scrollTop="+str((i+1)*70)
        browser.execute_script(js)
        # 每分钟倒计时65秒，每5秒显示剩余时长
        for j in range(13):
            print(65-j*5, end="")
            print(" " * 1, end="", flush=True)
            time.sleep(5)
        print('')
    # 关闭学习页面，切换句柄到积分目录
    time.sleep(2)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(handles[0])

# 主方法
use_cookie()


