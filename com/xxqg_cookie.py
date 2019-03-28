import json
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def main(cookies):
    browser = webdriver.Chrome()
    login_url = 'https://pc.xuexi.cn/points/my-points.html'
    browser.get(login_url)

    cookie_dict = {
        "domain": ".xuexi.cn",  # 火狐浏览器不用填写，谷歌要需要
        'name': '__UID__',
        'value': '181dac50-492b-11e9-a898-5ba8c5112414',
        "expires": 1584424786.759972,
        'path': '/',
        'httpOnly': False,
        'HostOnly': False,
        'Secure': False}
    browser.add_cookie(cookie_dict)
    cookie_dict2 = {
        "domain": ".xuexi.cn",  # 火狐浏览器不用填写，谷歌要需要
        'name': 'token',
        'value': '6ff8525f90b547dbb08eecaa3489cc1a',
        "expires": 1552910392.738832,
        'path': '/',
        'httpOnly': False,
        'HostOnly': False,
        'Secure': False}
    browser.add_cookie(cookie_dict2)



    login_url = 'https://pc.xuexi.cn/points/my-points.html'
    browser.get(login_url)


    time.sleep(10)


def get_session():

    login_url = 'https://pc.xuexi.cn/points/my-points.html'
    browser = webdriver.Chrome()
    browser.get(login_url)
    cookies = browser.get_cookies()

    print(cookies)
    time.sleep(2)

    js = "document.documentElement.scrollTop=700"
    browser.execute_script(js)

    # 显示等待，如title= “我的积分”，则结束倒计时，进行下一步
    print('请在60秒内扫码')

    try:
        WebDriverWait(browser, 60, 0.5).until(EC.title_is('我的积分'))
    except:
        print("没有人扫码啊，我走了")
        browser.quit()
        return
    cookies = browser.get_cookies()
    print(cookies)
    main(cookies)



if __name__ == '__main__':
    main(12)
    # get_session()