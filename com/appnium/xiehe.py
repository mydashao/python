# coding=utf-8
# 使用Python 代码驱动App 的方法
from appium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
server="http://127.0.0.1:4723/wd/hub"
desired_caps = {

                'platformName': 'Android',
                'deviceName': 'ALP-AL00',
                # apk包名
                'appPackage': 'com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy',
                # apk的launcherActivity
                'appActivity': 'com.hundsun.main.activity.SplashActivity'

                }

driver = webdriver.Remote(server, desired_caps)
time.sleep(20)
driver.find_element_by_id('com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/mainNaviLogo').click()