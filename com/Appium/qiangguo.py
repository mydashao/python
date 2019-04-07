# coding=utf-8
import time
from appium import webdriver
desired_caps = {
    "platformName": "Android",
    "deviceName": "ALP-AL00",
    "appPackage": "cn.xuexi.android",
    "appActivity": "com.alibaba.android.rimet.biz.SplashActivity"
                }

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(15)

# print(driver.page_source)
#
time.sleep(2)
# 允许存储权限
allow = driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button")
allow.click()
# print(driver.page_source)
# 开始挂号
print('开始挂号')
guahao = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]")
guahao.click()
# 须知 com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/regNoticeNextBtn

xuzhi = driver.find_element_by_id("com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/regNoticeNextBtn")
print(xuzhi.text)
xuzhi.click()
#  4.挂号地点选择 东区普通门诊
didian = driver.find_element_by_id("com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/hosDisEastCommon")
print(didian.text)
didian.click()
#   5.选择科室-内科
keshi1 = driver.find_element_by_id("com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/gridContentTxt")
print(keshi1.text)
keshi1.click()

# 6.选择二级科室-免疫内科门诊
keshi2 = driver.find_element_by_id("com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/gridContentTxt")
print(keshi2.text)
keshi2.click()

# 7.选择三级科室-免疫内科
keshi3 = driver.find_element_by_id("com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/gridContentTxt")
print(keshi3.text)
keshi3.click()

# 8.选择时间和专家：周四赵久良
expert = driver.find_element_by_id("com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/docName")
print(expert.text)
expert.click()
#  9.准备挂号
prepare_guahao = driver.find_element_by_id("com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/regBtn")

prepare_guahao.click()
print(prepare_guahao.text)



# el3 = driver.find_element_by_id("com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/userTvName")
# el3.send_keys("13810689366")
# el4 = driver.find_element_by_id("com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/userTvPsw")
# el4.send_keys("1qaz2wsx")
# el5 = driver.find_element_by_id("com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/userBtnLogin")
# el5.click()

'''
允许存储权限
id：com.android.packageinstaller:id/permission_allow_button
预约挂号
ID：com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/mainNaviLogo
挂号须知确认
ID：com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/regNoticeNextBtn
我xpath
/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout[4]/android.widget.LinearLayout/android.widget.ImageView
未登录 id
com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/userCenterIvLogo
用户名 id
com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/userTvName
密码 id
com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/userTvPsw
登陆
com.hundsun.qy.hospitalcloud.bj.xhhosp.hsyy:id/userBtnLogin



'''