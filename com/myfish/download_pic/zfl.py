from bs4 import BeautifulSoup
import random
import requests
from urllib import parse
import time

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
def get_html(url):

    headers = {'User-Agent': '', 'referer': 'link'}
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url, headers=headers)
    response.encoding = 'gb2312'
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    return soup

def main():
    main_url = 'https://zfl001.com/luyilu/'
    soup = get_html(main_url)
    url_list = soup.find_all('article',class_="excerpt")
    for url in url_list:
        topic_url = url.find('a',target="_blank")['href']
        full_url = 'https://zfl001.com'+topic_url
        topic(full_url)
        time.sleep(10)


def topic(url):
    print(url)
    soup = get_html(url)
    get_picture(soup)

    try:
        next_url = soup.find('li', class_='next-page').find('a')['href']
    except:
        next_url =  None

    if next_url != None:
        # index = find_last(url,"/")
        # next_urll = url[0:index]+next_url
        topic(parse.urljoin(url,next_url))
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
def get_picture(soup):
    pic_list = soup.find('article', class_="article-content").find_all('img')
    for pic in pic_list:
        pic_src = pic['src']
        print(pic_src)
        download(pic_src)

# 下载图片
def download(pic_src):
    folder_name = pic_src.split('/')[4]
    file_name = pic_src.split('/')[5]
    print(file_name)
    r = requests.get(pic_src)

    with open("D:\\pic\\"+file_name, 'wb') as f:
        f.write(r.content)

if __name__=="__main__":
    main()