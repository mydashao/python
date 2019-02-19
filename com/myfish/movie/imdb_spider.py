#每次爬虫结束时记录一个数值count写入记事本
#第二次继续爬的时候，读取这个数值，模100，计算在列表第几页（一页列表100条记录）
#直接到所在页面，继续爬虫
#excel文件实现续写

from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import random
import time
import pymysql
import tablib
import datetime

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

#url = 'https://www.imdb.com/user/ur7858364/ratings'
url=\
'https://www.imdb.com/user/ur7858364/ratings'
mylist = []
database =[]
count=0
date1=''
date2=''

#方法1：向网站发送请求，返回HTML对象
def get_html(url):
    headers = {'User-Agent': '', 'referer': 'link'}
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    return soup

# 方法2：获取IMDB评分列表中影片的某些属性
def get_list(list_url):
    soup = get_html(list_url)
    for tag in soup.find_all('div', class_='lister-item',limit=15):

        global count
        count = count + 1
        if count % 2 == 0:
            save_to_excel(mylist)

        title = tag.find('img')['alt']

        id = tag.find('div', class_='lister-item-image')['data-tconst']
        citle = get_douban_name(id)

        try:
            runtime = format_runtime(tag.find('span', class_='runtime').get_text())
        except AttributeError:
            runtime = ''
        try:
            genres = str(tag.find('span', class_='genre').get_text()).strip()
        except AttributeError:
            genres = ''
        IMDB_rate = float(tag.find('div', class_='ipl-rating-star').find('span',class_='ipl-rating-star__rating').get_text())
        my_rate = int(tag.find('div', {'class': 'ipl-rating-star ipl-rating-star--other-user small'}).find('span',class_='ipl-rating-star__rating').get_text())
        rate_date=format_rate_date(tag.find(lambda tag: tag.name == 'p' and tag.get('class') == ['text-muted']).get_text()[9:])

        mylist.append([id, title, citle, IMDB_rate, 0, 0, 0, 0, my_rate, genres,
             runtime, 'director', 'stars', 'budget', 'gross', 'production', 'release_date', 'watch_date', rate_date,'country'])




        print('==================== ' + str(count) + ' ====================')
        print('    片名    :' + title)
        print('    中文片名：'+citle)
        print('    ID      :' + id)
        print('    时长    :' + runtime)
        print('    类型    :' + genres)
        print('    IMDB评分:' + str(IMDB_rate))
        print('    我的评分 :' + str(my_rate))
        print('    评分日期 :' + rate_date)

        #get_citle(id)
        get_movie(id)
        get_movie_pro(id)
    try:
        next_url = soup.find('a', class_='lister-page-next')['href']
    except Exception :
        next_url = ''

    global url
    url = url[:21] + next_url
    time.sleep(30)

# 方法3：根据影片ID获取影片页面的某些属性
def get_movie(id):
    movie_url = "https://www.imdb.com/title/" + id + "/?ref_=rt_li_tt"
    soup = get_html(movie_url)
    try:
        vote = del_comon(soup.find('span', itemprop="ratingCount").text)
    except AttributeError:
        vote='10'
    try:
        director = soup.find('div', class_='credit_summary_item').find('a').get_text()
    except AttributeError:
        director=''
    stars = []
    global date1
    try:
        for actor in soup.find_all('td', class_='primary_photo',limit=10):
            stars.append(actor.find('img')['alt'])
    except AttributeError:
        stars = []

    try:
        release_date1 = format_release_date1(soup.find('a', {'title': 'See more release dates'}).get_text().strip())
        date1 = release_date1
    except AttributeError as E:
        release_date1 = ''
        date1=''
        print('------------date1-----------ERROR-')
    try:
        Meta_rate = soup.find('div', class_='metacriticScore').get_text().strip()
    except AttributeError:
        Meta_rate = ''

    production = []
    country=''
    for tags in soup.find_all('h4', class_='inline'):
        something = tags.get_text()
        if something == 'Country:':
            country = tags.find_parent().find('a').get_text().strip()
        if something == 'Production Co:':
            for co in tags.find_parent().find_all('a'):
                if co.get_text() != 'See more':
                    production.append(co.get_text().strip())


    print('    评分人数 :' + str(vote))
    print('    链接    :' + movie_url)
    print('    导演    :' + director)
    print('    演员    :'+','.join(stars))
    #print('    上映日期1:' + release_date1)
    print('    Metascore:'+ str(Meta_rate))
    print('    国家    :' + country)

    print('    制作公司：' +','.join(production))

    mylist[-1][4] = vote
    mylist[-1][5] = Meta_rate
    mylist[-1][6] = 0
    mylist[-1][7] = 0
    mylist[-1][11] = director
    mylist[-1][12] = ','.join(stars)
    mylist[-1][15] = ','.join(production)
    mylist[-1][17] = ''
    mylist[-1][19] = country

    time.sleep(5)


# 方法4：根据影片ID获取影片pro页面的某些属性
def get_movie_pro(id):
    movie_pro_url = "https://pro.imdb.com/title/" + id
    global date1
    global date2
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

    try:
        release_date2 = format_release_date2(soup.find('div', {'class': 'a-row a-spacing-base'}).find('span', {'class': 'a-declarative'}).get_text().strip().replace('\n',''))
        date2 = release_date2
    except AttributeError:
        release_date2=''
        date2 = ''
    release_date = compare_release_date(date1,date2)

    # release_date = release_date
    # print(len(release_date))
    # count = 0
    # for i in range(len(release_date)):
    #     count =count+1
    #     print(str(count)+':'+ release_date[i])
    #print(release_date)
    print('    投资:' + budget)
    print('    票房:' + gross)
    #print('    上映日期：'+release_date2)
    print('    上映日期1:' + date1)
    print('    上映日期2:' + date2)
    print('    上映日期：'+release_date)

    mylist[-1][13] = money_to_int(budget)
    mylist[-1][14] = money_to_int(gross)
    mylist[-1][16] = release_date
    date1 = ''
    date2 = ''
    time.sleep(5)


# 方法5：根据影片ID获取imdb.cn网站的影片的中文影片名
def get_imdbcn_citle(id):
    citle_url = "http://www.imdb.cn/title/"+id
    soup = get_html(citle_url)
    citle = soup.find('div',class_='fk-3').find('h3').get_text()
    print('    片名:'+citle)



# 方法6：根据影片ID，通过数据库获取影片豆瓣ID
def get_douban_name(id):
    db = pymysql.connect(host='localhost', user='root', password='777748', port=3306, db='movie')
    cursor = db.cursor()
    sql = "SELECT ID,AKA,Citle FROM douban where IMDB_id='"+id+"'"
    print(sql)
    try:
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
           aka = str(data[1])
           citle = str(data[2])
           if aka != None:
               return aka
           else:
               return citle
        else:
            return ''
    except Exception as e:
        print(e)
        return ''


# # 方法7：根据豆瓣ID，获取豆瓣页面的影片信息
# def get_douban_info(douban_id):
#     citle_url = "https://movie.douban.com/subject/" + douban_id + "/"
#     soup = get_html(citle_url)
#     citle = soup.find('title').get_text()[:-5].strip()


# 方法8：将获取的信息保存到数据库
def save_to_database1():
    db = pymysql.connect(host='localhost', user='root', password='777748', port=3306, db='movie')
    cursor = db.cursor()
    try:
        # for i in range(3):
        #     sql = "INSERT INTO movies " \
        #           "(ID, title, citle, IMDB_rate, vote, Meta_rate, Mtime_rate, douban_rate, my_rate, genres," \
        #           "runtime, director, stars, budget, gross, production, release_date, watch_date, rate_date) VALUES " \
        #           "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE " \
        #           "IMDB_rate=" + "'" + mylist[i][3] + "'",\
        #           "vote=" + "'" + mylist[i][4] + "'",\
        #           "Meta_rate=" + "'" + mylist[i][5] + "'",\
        #           "Mtime_rate=" + "'" + mylist[i][6] + "'",\
        #           "douban_rate=" + "'" + mylist[i][7] + "'",\
        #           "my_rate=" + "'" + mylist[i][8] + "'",\
        #           "budget=" + "'" + mylist[i][13] + "'",\
        #           "gross=" + "'" + mylist[i][14] + "'",\
        #           "rate_date=" + "'" + mylist[i][18] + "'",\
        #
        #
        #
        #     cursor.execute(sql, (mylist[i][0],mylist[i][1],mylist[i][2],mylist[i][2],mylist[i][2],mylist[i][2],mylist[i][2],mylist[i][2],mylist[i][2],mylist[i][2]))

        for i in range(3):
            sql = "INSERT INTO movies " \
                  "(ID, title, citle, IMDB_rate, vote, Meta_rate, " \
                  "Mtime_rate, douban_rate, my_rate, genres, runtime,  director, " \
                  "stars, budget, gross, production, release_date, watch_date, rate_date) VALUES " \
                  "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE " \
                  "title=" + "'" + mylist[i][1] + "',"\
                  "vote=" + "'" +str(mylist[i][4]) + "',"\
                  "Meta_rate=" + "'" + str(mylist[i][5]) + "',"\
                  "Mtime_rate=" + "'" + str(mylist[i][6] )+ "',"\
                  "douban_rate=" + "'" + str(mylist[i][7]) + "',"\
                  "my_rate=" + "'" +str( mylist[i][8]) + "',"\
                  "budget=" + "'" + str(mylist[i][13]) + "',"\
                  "gross=" + "'" + str(mylist[i][14]) + "'"\



            cursor.execute(sql, (mylist[i][0],mylist[i][1],mylist[i][2],mylist[i][3],mylist[i][4],mylist[i][5],
                                 mylist[i][6],mylist[i][7],mylist[i][8],mylist[i][9],mylist[i][10],mylist[i][11],
                                 mylist[i][12], mylist[i][13],mylist[i][14],mylist[i][15],mylist[i][16],mylist[i][17],mylist[i][18]))

            print(sql)
            print('Successful')
            db.commit()
    except Exception as e:
        print('错误')
        print(e)

        db.rollback()
    db.close()




# 方法10：将获取的信息保存到excel
def save_to_excel(mylist):

    headers = (
    'ID', 'title', 'citle', 'IMDB_rate', 'vote', 'Meta_rate', 'Mtime_rate', 'douban_rate', 'my_rate', 'genres',
    'runtime', 'director', 'stars', 'budget', 'gross', 'production', 'release_date', 'watch_date', 'rate_date','country')
    print(mylist)

    mylist = tablib.Dataset(*mylist, headers=headers)

    with open('D:\IMDB.xlsx', 'wb') as f:
        f.write(mylist.export('xlsx'))
#在指定行插入一行数据
#mylist.insert(0, ['est', 'liuyi','test','test','test','test5'])
#这个语句的意思在第1行插入一行数据，数据的个数和列数相等，注意标题行不算在内，从有数据的行开始算行数

def format_rate_date(date):
    date_format = datetime.datetime.strptime(date, '%d %b %Y').strftime('%Y-%m-%d')
    return date_format


def format_release_date1(date1):
    try:
        x = date1.find("(")
        date1 = date1[:x].strip()
        print(date1)

        date1_format = datetime.datetime.strptime(date1, '%d %B %Y').strftime('%Y-%m-%d')
        return date1_format
    except ValueError:
        return ''


def format_release_date2(date2):
    try:
        print(date2)
        date2 = date2.replace(',', ' ')
        date2 = date2[0:3] + ' ' + date2[3:]
        date2_format = datetime.datetime.strptime(date2, '%b %d %Y').strftime('%Y-%m-%d')
        return date2_format
    except ValueError:
        return ''

def compare_release_date(date1,date2):
    if (date1=='') and(date2!=''):
        return date2
    elif (date2=='') and(date1!=''):
        return date1
    elif (date2=='') and(date1==''):
        return ''
    elif date1 > date2:
        return date2
    else:
        return date1

def format_runtime(runtime):
    try:
        return str(int(float(runtime[0:1]))*60+int(float(runtime[5:7])))
    except ValueError:
        return ''



def money_to_int(string):
    money =string.replace(',','')
    if money=='':
        return ''
    elif money[0] == '￥':
        return str(int(money[1:])/6.7)
    elif money[0] == '£':
        return str((int(money[1:])*1.3))
    elif money[0] == '$':
        return str(int(money[1:]))

#解决数字的逗号问题
def del_comon(string):
    string =string.replace(',','')
    return int(string)

for i in range(13):
    print(url)
    get_list(url)
    save_to_excel(mylist)
    #save_to_database1()






# (0'ID',1'title',2'citle',3'IMDB_rate',4'vote',
# 'Meta_rate','Mtime_rate','douban_rate','my_rate','type',
# 'runtime','director','stars','budget','gross',
# 'production','release_date','watch_date','rate_date')
