from selenium import webdriver
import time
import datetime
import threading
begin_list = [1,2,3,4,5,6,7,8,9,10]


def ticket_old():
    threads = []

    for i in range(len(begin_list)):
        threads.append(threading.Thread(target=refresh_old, args=(time,begin_list[i])))

    for t in threads:
        # t.setDaemon(True)
        t.start()


def refresh_old(time,chrome):
    browser = webdriver.Chrome()

    for i in range(8):
        browser.execute_script('window.open()')
        print(chrome,'打开第',i+1,'个页面')
        time.sleep(1)

    handles = browser.window_handles
    url = 'https://www.baidu.com'
    for times in range(100):
        for j in range(len(handles)):
            browser.switch_to.window(handles[j])
            browser.get(url)
            print(str(datetime.datetime.now())[:-3],'第',chrome,'个浏览器打开第',j+1,'个页面刷新第',times+1, '次')
            time.sleep(1)


if __name__ == "__main__":
    main()