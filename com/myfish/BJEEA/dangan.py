
from selenium import webdriver
import time
import random
import requests
from bs4 import BeautifulSoup

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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


def get_session():

    login_url = 'http://222.249.128.17/app/dangan/login.asp'

    # option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    #browser = webdriver.Chrome(chrome_options=option)
    browser = webdriver.Chrome()
    browser.get(login_url)
    #print(browser.page_source)
    username = browser.find_element_by_name('username')
    username.send_keys('pany')
    password = browser.find_element_by_name('pwd')
    password.send_keys('bjeea888')
    submit = browser.find_element_by_name('B1')
    submit.click()
    time.sleep(1)

    js = "window.open('ht_index2.asp?id=11227&tm=文号文件&bgqx=永久&quanxian=3')"

    browser.execute_script(js)
    time.sleep(1)

    cookies = browser.get_cookies()

    print(cookies)
    return cookies


    # handles = browser.window_handles
    # browser.switch_to.window(handles[-2])
    # print(browser.page_source)
    # print(browser.current_url)


def use_cookie(url):
    cookiestr = get_session()
    print(cookiestr[0])
    browser = webdriver.Chrome()
    browser.get('http://222.249.128.17/app/dangan/login.asp')

    browser.add_cookie(cookiestr[0])
    browser.get(url)
    print(browser.page_source)
    time.sleep(3)
    wenhao = browser.find_element_by_name('wh')
    wenjianming = browser.find_element_by_name('tm')
    zerenren = browser.find_element_by_name('zrz')
    riqi = browser.find_element_by_name('rq')
    submit = browser.find_element_by_name('bc')
    wenhao.send_keys('pany')
    time.sleep(3)

    wenjianming.send_keys('pany')
    time.sleep(3)

    zerenren.send_keys('pany')
    time.sleep(3)

    riqi.send_keys('2006-06-01')
    time.sleep(3)

    submit.click()
    time.sleep(3)



    # # headers['User-Agent'] = random.choice(user_agent_list)
    # s  = requests.Session()
    #
    # for cookie in cookiestr:
    #     s.cookies.set(cookie['name'], cookie['value'])
    #     print(s.cookies)
    #
    # response = s.get(url)
    # response.encoding = 'GBK'
    # html = response.text
    # soup = BeautifulSoup(html, "lxml")
    # print('--------------------------------------------------')
    # print(html)
    # return soup


url = 'http://222.249.128.17/app/dangan/ht_index2.asp?id=11322&tm=%B2%E2%CA%D4%B0%B8%BE%ED&bgqx=%D3%C0%BE%C3&quanxian=3'

use_cookie(url)


