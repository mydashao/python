from selenium import webdriver

import time
import requests
from bs4 import BeautifulSoup
import requests
import re
import json

browser = webdriver.Chrome()

browser.get('http://www.baidu.com')
print('打开百度：'+browser.current_window_handle)
time.sleep(5) 

js = "window.open('http://www.taobao.com')"
browser.execute_script(js)
print('打开淘宝：'+browser.current_window_handle)

time.sleep(5) 
js = "window.open('http://www.sohu.com')"
browser.execute_script(js)
print('打开搜后：'+browser.current_window_handle)

time.sleep(5) 
js = "window.open('http://www.douban.com')"
browser.execute_script(js)
print('打开豆瓣：'+browser.current_window_handle)

time.sleep(5) 
browser.switch_to_window(browser.window_handles[-1])
print('切换到豆瓣：'+browser.current_window_handle)
time.sleep(5)

browser.close()
browser.switch_to_window(browser.window_handles[-1])

print('关闭豆瓣：'+browser.current_window_handle)
time.sleep(5) 

browser.close()
browser.switch_to_window(browser.window_handles[-1])
time.sleep(5)

print('关闭下一个：'+browser.current_window_handle)
time.sleep(5)

browser.close()
browser.switch_to_window(browser.window_handles[-1])

print('关闭下一个：'+browser.current_window_handle)
time.sleep(5)


#
#
# handles = browser.window_handles
# browser.switch_to.window(handles[1])
# print('this is 1 ')
# time.sleep(5)
#
#
# browser.switch_to.window(handles[0])
# print('this is 0')
#
# time.sleep(5)
# browser.switch_to.window(handles[1])
# print('this is 1 ')
# time.sleep(5)
# browser.switch_to.window(handles[-1])
# print('this is -1')
#
# time.sleep(5)
#
# browser.switch_to.window(handles[2])
# print('this is 2')
# time.sleep(5)
# browser = webdriver.Chrome()
# browser.get('https://www.bjeea.cn/')
# print(browser.page_source)
#
# print(browser.find_element_by_xpath("//title"))
# text11 = browser.find_element_by_xpath("//title").text
# print(text11)
#
#
#                 https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/data5957f69bffab66811b99940516ec8784.js
# 重要新闻	https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/5957f69bffab66811b99940516ec8784.html
# 重要活动	https://www.xuexi.cn/c06bf4acc7eef6ef0a560328938b5771/9a3668c13f6e303932b5e0e100fc248b.html
# 重要会议	https://www.xuexi.cn/89acb6d339cd09d5aaf0c2697b6a3278/    9a3668c13f6e303932b5e0e100fc248b.html
#                 https://www.xuexi.cn/89acb6d339cd09d5aaf0c2697b6a3278/data9a3668c13f6e303932b5e0e100fc248b
#
# 重要讲话	https://www.xuexi.cn/588a4707f9db9606d832e51bfb3cea3b/9a3668c13f6e303932b5e0e100fc248b.html
# 重要文章	https://www.xuexi.cn/6db80fbc0859e5c06b81fd5d6d618749/9a3668c13f6e303932b5e0e100fc248b.html
# 出国访问	https://www.xuexi.cn/2e5fc9557e56b14ececee0174deac67f/9a3668c13f6e303932b5e0e100fc248b.html
# 指示批示	https://www.xuexi.cn/682fd2c2ee5b0fa149e0ff11f8f13cea/9a3668c13f6e303932b5e0e100fc248b.html
# 函电致辞	https://www.xuexi.cn/13e9b085b05a257ed25359b0a7b869ff/9a3668c13f6e303932b5e0e100fc248b.html
# 新时代纪实	https://www.xuexi.cn/9ca612f28c9f86ad87d5daa34c588e00/9a3668c13f6e303932b5e0e100fc248b.html
# 学习时评	https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html
# 综合新闻	https://www.xuexi.cn/7097477a9643eacffe4cc101e4906fdb/9a3668c13f6e303932b5e0e100fc248b.html

# res = requests.get("https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/datab87d700beee2c44826a9202c75d18c85.js")
# res.encoding = 'utf-8'
# print(res.text)
# for key,value in json.loads(res.text.lstrip('globalCache = ').rstrip(';'),encoding="utf-8").items():
#     if key != 'sysQuery':
#         for item in  value['list']:
#             print(item['static_page_url'],item['frst_name'])
# 
# for i in range(24):
#     print(i)