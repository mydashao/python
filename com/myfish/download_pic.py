
from selenium import webdriver
import time
url = 'https://zfl001.com/luyilu/2019/0317/6722.html'

browser = webdriver.Chrome()
browser.get(url)
time.sleep(5)
#
# js="var q=document.documentElement.scrollTop=900"
# browser.execute_script(js)
# time.sleep(5)
print(browser.page_source)
