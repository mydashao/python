from bs4 import BeautifulSoup
import random
import requests
from urllib import parse
import time
import os
from urllib.parse import quote
import  string

LOG = "D:\pic\log.txt"
keyword={'土肥圆','周妍希','乔依琳','小鸟酱','蕾丝兔','爱丝','假面女皇','无忌影社','私人玩物','麻酥酥',
         '蜜桃社','极品露出','李妍曦','若兮','完具少女','尤妮丝','尤蜜荟','Toxic','宇航员','闫盼盼'}
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
main_url = 'https://so.azs2019.com'
url1 = '/serch.php?keyword='

# 根据url返回soup对象
def get_html(url):

    headers = {'User-Agent': '', 'referer': 'link'}
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url, headers=headers)
    response.encoding = 'GBK'
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    return soup

# URL中文字符转换
def uri(key):
    return quote(key.encode('GBK'), safe=string.printable)

# 主方法，遍历keyword列表中的元素，用元素作为url中keyword的参数
def main():
    for key in keyword:
        uri_key = uri(key)
        url = main_url+url1+uri_key
        print(url)
        get_keyword(url)

# 得到一个keyword元素的所有url，如果存在log中就跳过，如果不在log中，调用topic方法下载，最后获取本页面的下一页链接，抓取下一页
def get_keyword(urls):
    soup = get_html(urls)
    url_list = soup.find_all('article',class_="excerpt")
    for url in url_list:
        title = url.find('h2').a.attrs['title']
        # print(title)
        topic_url = url.find('a',target="_blank")['href']
        topic_url = topic_url[topic_url.find('com')+3:]

        # print(full_url)
        if topic_url in get_log():
            print(title, '已存在')
            continue
        else:
            full_url = 'https://zfl001.com' + topic_url
            print(title, '开始下载')
            topic(title, full_url)
            save_log(topic_url)


    try:
        next_page = soup.find('li',class_="next-page").a['href']
        if next_page:

            next_page_url = main_url+uri(next_page)
            print(next_page_url)
            get_keyword(next_page_url)
    except:
        return

# 获取单keyword单个url的所有图片，通过get_picture方法下载图片，如果下一页不为空，循环递归
def topic(title,url):
    # print(url)
    soup = get_html(url)
    time.sleep(5)

    get_picture(soup,title)

    try:
        next_url = soup.find('li', class_='next-page').find('a')['href']
        next = soup.find('li', class_='next-page').get_text()
    except:
        next_url =  None

    if next_url != None:
        # index = find_last(url,"/")
        # next_urll = url[0:index]+next_url
        next_full_url = parse.urljoin(url,next_url)
        # print(next_full_url)
        topic(title,next_full_url)

    else :
        print(' ')


def find_last(string,str):
    last_position=-1
    while True:
        position = string.find(str, last_position + 1)
        if position==-1:
            return last_position
            last_position=position



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

# 保存日志
def save_log(url):
    # logger.debug('     开始保存cookie')
    time.sleep(1)

    with open(LOG, 'a+') as f:
        f.write(url+"\n")
    time.sleep(1)

# 读取日志
def get_log():
    result=[]
    # logger.debug('     开始读取cookie')
    time.sleep(1)
    with open(LOG, 'r') as f:
        for line in f:
            result.append(line.strip('\n'))
        return result

if __name__=="__main__":
    main()