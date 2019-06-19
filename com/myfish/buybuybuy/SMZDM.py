from selenium import webdriver

def login():
    # 打开领券页面
    login_url = 'https://www.smzdm.com/p1/'
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(login_url)
    print(browser.page_source)

    # 获得已保存的cookie


login()