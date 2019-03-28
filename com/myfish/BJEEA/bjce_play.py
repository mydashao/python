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

def main():
    login()

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
        'http://el.bjce.gov.cn/elms/gjwweb/personspace/listCheckedCourse.action')
    time.sleep(6)
    play(browser)


def work(page,browser):

    print(browser.page_source)
    kejian_list = browser.find_elements_by_class_name('table-xuexi')
    for kejian in kejian_list:
        try:
            title = kejian.find_element_by_class_name('p_l_10')
            print('     第',count,'课：',title, end="")
            play_but =kejian.find_element_by_tag_name('a').get_attribute('onclick')
            play(browser)



            count = count+1



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

def play(browser):
    print()

    js = "window.open('studyCourse.action?courseId=190591931&userId=20176013&coursenum=HSWL2018108&stamp=1553474505901&studySource=1')"
    browser.execute_script(js)

    url = "http://el.bjce.gov.cn/elms/gjwweb/personspace/broadcastCourse.action?coursenum=HSWL2018108&centerClassCourse=null&win=null"
    time.sleep(10)
    browser.execute_script(js)

if __name__ == "__main__":
    main()
