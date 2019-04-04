from bs4 import BeautifulSoup
import random
import requests
from urllib import parse
import time
import os

# TODO:记录下载的title，保存到txt中，每次下载前先比对，如果页面title不在txt就下载，如果title在txt就跳过
LOG = "D:\pic\log.txt"
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
# 请求url的方法
main_url = 'https://zfl001.com/luyilu/'
def get_html(url):

    headers = {'User-Agent': '', 'referer': 'link'}
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url, headers=headers)
    response.encoding = 'GBK'
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    return soup

def main(urls):
    soup = get_html(urls)
    url_list = soup.find_all('article',class_="excerpt")
    for url in url_list:
        title = url.find('h2').string
        topic_url = url.find('a',target="_blank")['href']
        full_url = 'https://zfl001.com'+topic_url
        if topic_url not in get_log():
            print(title,'开始下载')
            topic(title,full_url)
            print('')
            save_log(topic_url)
            time.sleep(10)
        else:
            print(title,'已存在')
    next_page = soup.find('li',class_="next-page").a['href']
    if next_page:
        print(main_url+next_page)
        main(main_url+next_page)


def topic(title,url):
    # print(url)
    soup = get_html(url)
    get_picture(soup,title)

    try:
        next_url = soup.find('li', class_='next-page').find('a')['href']
    except:
        next_url =  None

    if next_url != None:
        # index = find_last(url,"/")
        # next_urll = url[0:index]+next_url
        topic(title,parse.urljoin(url,next_url))
        time.sleep(5)
    else:
        return

def find_last(string,str):
    last_position=-1
    while True:
        position = string.find(str, last_position + 1)
        if position==-1:
            return last_position
            last_position=position


# def get_next(soup):
#     try:
#         next = soup.find('li', class_='next-page').find('a')['href']
#         next_url='https://zfl001.com/luyilu/' + next
#         return next_url
#     except:
#         return None


# 获取图片url
def get_picture(soup,title):
    pic_list = soup.find('article', class_="article-content").find_all('img')
    for pic in pic_list:
        pic_src = pic['src']
        # print(pic_src)
        download(pic_src,title)


# 下载图片
def download(pic_src,title):
    folder_name = title
    file_name = pic_src.split('/')[5]
    # print(file_name)
    print('\r', file_name, end='',flush=True)

    r = requests.get(pic_src)
    path = "D:\\pic\\"+folder_name
    if os.path.exists(path) is False:
        os.makedirs(path)

    with open(path+'\\'+file_name, 'wb') as f:
        f.write(r.content)

def save_log(url):
    # logger.debug('     开始保存cookie')
    time.sleep(1)

    with open(LOG, 'a+') as f:
        f.write(url+"\n")
    time.sleep(1)

# 获取程序保存在COOKIE_FILE中的cookie
def get_log():
    result=[]
    # logger.debug('     开始读取cookie')
    time.sleep(1)
    with open(LOG, 'r') as f:
        for line in f:
            result.append(line.strip('\n'))
        return result

if __name__=="__main__":
    main(main_url)