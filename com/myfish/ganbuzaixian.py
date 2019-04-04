import json
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
count=0

def login():
    url = 'http://www.bjce.gov.cn/'
    list_url = 'http://el.bjce.gov.cn/elms/gjwweb/coursemarket/courseMarketManagerFrame.action?code=null&fenlID=null&courseSigns=1'
    index_url = "http://el.bjce.gov.cn/elms/gjwweb/coursemarket/courseMarketManagerFrame.action?code=null&fenlID=null&courseSigns=1"
    browser = webdriver.Chrome()
    browser.get(url)
    browser.switch_to.frame('frame_content')
    browser.switch_to.frame('userLogin_frame')

    browser.find_element_by_name('keyWord2').send_keys("40215963")
    time.sleep(2)
    browser.find_element_by_name('password').send_keys("8888")
    time.sleep(2)

    action = ActionChains(browser)
    action.send_keys(Keys.ENTER)
    action.perform()
    time.sleep(5)
    print('成功登录')
    browser.get(
        'http://el.bjce.gov.cn/elms/gjwweb/coursemarket/listNewCourseAction.action?stamp=1553424249743&courseSigns=')
    time.sleep(6)
    work(1,browser)


def work(page,browser):

    # handles = browser.window_handles
    # browser.switch_to.window(handles[-1])
    # print(browser.page_source)
    kejian_list = browser.find_elements_by_class_name('kejian_tuwen_bg')
    for kejian in kejian_list:
        try:
            global count
            count = count+1
            title = kejian.find_element_by_class_name('red14_b').text
            print('     第',count,'课：',title, end="")
            type = kejian.find_element_by_tag_name('img').get_attribute('title')
            # print ('     ',type)
            if type == '学习达到规定时长获得学时':
                add_kejian(browser)
            else:
                print('------需要考试！！！')

            # try:
            #     xue = kejian.find_element_by_xpath('//img[@src="./skin/JazzBlue/images/xue.png"]').get_attribute('title')
            #     kao = kejian.find_element_by_xpath('//img[@src="./skin/JazzBlue/images/kao.png"]').get_attribute('title')
            #
            #     print('     ',xue)
            #     add_kejian(browser)
            # except Exception as e:
            #     print('     需要考试！！！')
            #     print(e)
        except Exception as e:
            browser.refresh()
            work(page, browser)

    page = page+1
    browser.find_element_by_name('toPage').clear()
    time.sleep(1)
    browser.find_element_by_name('toPage').send_keys(page)
    time.sleep(1)
    browser.find_element_by_name('pageGoto').click()
    time.sleep(10)
    work(page, browser)

def add_kejian(browser):
    browser.find_element_by_class_name('kejian_bt1').click()
    print('------已添加')



login()