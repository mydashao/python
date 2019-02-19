from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import random
import time
import pymysql
import tablib

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

url = 'https://www.imdb.com/user/ur7858364/ratings'
mylist = []

def get_list(list_url):

    soup = get_html(list_url)
    for tag in soup.find_all('div', class_='lister-item',limit=2):
        title = tag.find('img')['alt']
        id = tag.find('div', class_='lister-item-image')['data-tconst']
        runtime = tag.find('span', class_='runtime').get_text()
        genres = str(tag.find('span', class_='genre').get_text()).strip()
        IMDB_rate = tag.find('div', class_='ipl-rating-star').find('span',class_='ipl-rating-star__rating').get_text()
        my_rate = tag.find('div', {'class': 'ipl-rating-star ipl-rating-star--other-user small'}).find('span',class_='ipl-rating-star__rating').get_text()
        rate_date=tag.find(lambda tag: tag.name == 'p' and tag.get('class') == ['text-muted']).get_text()

        mylist.append([title,id,IMDB_rate,my_rate,rate_date])

        print('    片名    :' + title)
        print('    ID      :' + id)
        print('    时长    :' + runtime)
        print('    类型    :' + genres)
        print('    IMDB评分:' + IMDB_rate)
        print('    我的评分 :' + my_rate)
        print('    评分日期 :' + rate_date)

        get_movie(id)
        get_movie_pro(id)
    next_url = soup.find('a', class_='lister-page-next')['href']

    global url
    url = url[:21] + next_url
    time.sleep(1)


def get_movie(id):
    movie_url = "https://www.imdb.com/title/" + id + "/?ref_=rt_li_tt"
    soup = get_html(movie_url)

    print('    评分人数：' + soup.find('span', itemprop="ratingCount").text)
    print('    链接：' + movie_url)
    print('    导演：' + soup.find('div', class_='credit_summary_item').find('a').get_text())
    print('    演员：', end='')

    for actor in soup.find_all('td', class_='primary_photo'):
        print(actor.find('img')['alt'], end='')
        print(',', end='')
    print('')
    for money in soup.find_all('h4', class_='inline'):
        something = money.get_text()

        # if something == 'Budget:':
        #     print('    投资：' + money.next_sibling.strip())
        # elif something == 'Cumulative Worldwide Gross:':
        #     print('    票房：' + money.next_sibling.strip())
        #
        if something == 'Production Co:':
            print('    制作公司：', end='')
            for co in money.find_parent().find_all('a'):
                if co.get_text() != 'See more':
                    print(co.get_text().strip(), end='')
                    print(',', end='')
            print('')

    print('    上映日期：' + soup.find('a', {'title': 'See more release dates'}).get_text().strip())
    try:
        print('    Metascore 评分：' + soup.find('div', class_='metacriticScore').get_text().strip())
    except AttributeError:
        print('    Metascore 评分：无')

    time.sleep(5)


def get_movie_pro(id):
    movie_pro_url = "https://pro.imdb.com/title/" + id

    soup = get_html(movie_pro_url)
    try:
        gross = soup.find('div', {'class': 'a-section a-spacing-small gross_world_summary'}).find('div', {
        'class': 'a-column a-span5 a-text-right a-span-last'}).get_text().strip()
    except AttributeError:
        gross = ''
    try:
        budget = soup.find('div', {'class': 'a-section a-spacing-small budget_summary'}).find('div', {
        'class': 'a-column a-span5 a-text-right a-span-last'}).get_text().strip()
    except AttributeError:
        budget = ''
    release_date = soup.find('div', {'class': 'a-row a-spacing-base'}).find('span', {'class': 'a-declarative'}).get_text().strip().replace('\n','')
    # release_date = release_date
    # print(len(release_date))
    # count = 0
    # for i in range(len(release_date)):
    #     count =count+1
    #     print(str(count)+':'+ release_date[i])
    #print(release_date)
    print('    投资:' + budget)
    print('    票房:' + gross)
    print('    上映日期：'+release_date)


    print('-----------------------------------------------')
    time.sleep(5)

def get_html(url):
    headers = {'User-Agent': '', 'referer': 'link'}
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    return soup

#解决数字的逗号问题
# def del_comon(number):
#     string =int(number.replace(',',''))
#     return str(string)



for i in range(1):
    print(url)
    get_list(url)

headers = ('df ','色','围绕多试点范围324','efe','2wdwd')
print(mylist)
mylist = tablib.Dataset(*mylist, headers=headers)
#print(mylist.csv)
with open('D:\IMDB.xlsx', 'wb') as f:
    f.write(mylist.xlsx)
