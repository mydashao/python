import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

def text():
    # # 新建一个浏览器
    # browserC = webdriver.Chrome()
    # # 打开页面
    # browserC.get('https://www.xuexi.cn/70e1f76094ce39682454e784074eca04/cf94877c29e1c685574e0226618fb1be.html')
    #
    # print('新建浏览器的句柄：'+browserC.current_window_handle)
    # url = browserC.find_element_by_class_name('prism-player').find_element_by_tag_name('video').get_attribute('src')
    # print(url)
    # # 浏览器新建一个页面
    # browserC.execute_script("window.open()")
    #
    # handle = browserC.current_window_handle
    # browserC.switch_to_window(handle[1])
    #
    # # 切换句柄到新建页面
    # # 新建页面中打开url
    # browserC.get('http://www.baidu.com')
    # print('新建页面后的句柄：'+browserC.current_window_handle)
    # # 新建句柄
    # handle = browserC.current_window_handle
    # # 切换句柄到新建页面
    # browserC.switch_to_window(handle[1])
    # print('切换页面后的句柄：'+browserC.current_window_handle)
    #
    #
    # time.sleep(8)


    str = '10分/10分'
    had = str.split("/")[0]
    had = had[:-1]
    print(had)


text()