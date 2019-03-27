
# # 随机选取视频和文章
# # 获取视频长度，新闻联播
# # 判断不自动播放是否计算分数
#
# from selenium.webdriver.common.action_chains import ActionChains
#
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# import json
# import time
# import random
# import requests
# from bs4 import BeautifulSoup
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
#
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
#
# # 常量，阅读观看等时长，单位分钟
# READ=2
# WATCH = 2
# READ_TIME = 5
# WATCH_TIME = 5
#
# user_agent_list = [
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
#     "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
#     ]
#
# # 调用cookie方法，尚未完成
#
#
def get_session():
     print(int(5/2))
#
#     login_url = "https://www.xuexi.cn/70e1f76094ce39682454e784074eca04/cf94877c29e1c685574e0226618fb1be.html"
#     # login_url ="https://www.bilibili.com/video/av16041375/"
#
#     browser = webdriver.Chrome()
#     browser.get(login_url)
#     print(browser.page_source)
#     time.sleep(2)
#
#     video = browser.find_element_by_tag_name("video")
#     duration = browser.find_element_by_class_name("duration").text.strip()
#     print(duration)
#
#     url = browser.execute_script("return arguments[0].currentSrc;", video)
#     time.sleep(2)
#     action = ActionChains(browser)
#     action.send_keys(Keys.TAB)
#     action.perform()
#     print(url)
#     # print("load")
#     # browser.execute_script("return arguments[0].load()", video)
#     # time.sleep(10)
#     print("play")
#     browser.execute_script("return arguments[0].play()", video)
#
#     time.sleep(10)
#     print("stop")
#
#     browser.execute_script("return arguments[0].pause()", video)
#     time.sleep(3)
#
#     # xwlb = 'https://www.xuexi.cn/9b202c09ea962c54c625cdd0e272bd2a/data577a3dee30fbeb9ab03295a860c2a295.js'
#     # # xwlb = 'https://www.xuexi.cn/c2937d45fb9599f30d22bbe62a9168dc/data7f9f27c65e84e71e1b7189b7132b4710.js'
#     # res = requests.get(xwlb)
#     # res.encoding = 'utf-8'
#     # # print(res.text)
#     # url_list = []
#     # for key, value in json.loads(res.text.lstrip('globalCache = ').rstrip(';'), encoding="utf-8").items():
#     #     if key != 'sysQuery':
#     #         for item in value['list']:
#     #             print(item['static_page_url'], item['frst_name'], item['original_time'])
#     #             url_list.append(item['static_page_url'])
#     #         size = len(url_list)
#     #         url = url_list[int(random.randint(1, size - 1))]
#     #         print(url)



# 主方法
get_session()



