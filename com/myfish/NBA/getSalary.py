import requests
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urlencode
base_url = 'http://www.stat-nba.com/player/'

#得到三分页面信息
def get_html():

    params={
        'QueryType':'all',
        'AllType':'season',
        'AT':'tot',
        'order':'1',
        'crtcol':'threep',
        'PageNum':'100',
        'Threep0':'1500',
        'Threep1':'4000'
    }

    base_url = 'http://www.stat-nba.com/query.php?'
    url=base_url+urlencode(params)
    response = requests.get(url)
    response.encoding='utf-8'
    #print(response.status_code)
    if response.status_code == 200:
        return response.text
    else:
        print('发生错误')

#分局三分页面信息，得到三分射手的ID
def get_player(html,no):

    soup=BeautifulSoup(html,'lxml')
    for id in soup.select('.query_player_name'):

        player = id.get_text()
        seri = int(id['href'][9:][:-5])
        no = no+1
        print('序号:'+str(no)+'---', end=' ')
        print('ID:'+str(seri)+'---'+player, end=' ')
        print('---', end=' ')
        #根据射手ID得到射手页面HTML
        HTML = get_salary(seri)
        #根据页面解析有用信息
        get_useful_info(HTML)
        time.sleep(2)


#获取html
def get_salary(seri):

    url = base_url+str(seri)+'.html'
    print(url, end=' ')
    print('---', end=' ')
    response = requests.get(url)
    response.encoding='utf-8'
    if response.status_code == 200:
        #print(response.text)
        return response.text
        #response.json()
        #print(j)

#解析HTML
def get_useful_info(html):
    soup=BeautifulSoup(html,'lxml')
    # name =soup.find('title').string
    # sp = '|'
    # name=name[0:name.find(sp)]
    # print(name, end=' ')
    # print('---', end=' ')
    #显示总数，如果大于1500显示出来
    for threep in (soup.select('.stat_box tr td.normal.threep')):
        #print(threep.get_text())
        ifthousand = int(float(threep.get_text()))
        if(ifthousand>1000):
            print('总计:' +str(ifthousand))
        #print(soup.find('title').string)
            for three in soup.select('#stat_box_tot .normal.threep.change_color.col9'):
                print(three.get_text(), end=' ')
                print('-', end=' ')
            print('')
            break



    #print(soup.select('.stat_box tbody .sort .normal.threep').get_text())
    #print(soup.find_all(class_='normal threep')[3])





#写入文件
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as c:
        c.write(json.dumps(content,ensure_sacii=False)+ '\n')

if __name__== '__main__':
    no = 0
    get_player(get_html(),no)

    #get_useful_info(get_salary(seri))
    #get_useful_info(get_salary(527))


    # for i in range(100):
    #    try:
    #        get_useful_info(get_salary(i+1))
    #        print('')
    #        time.sleep(5)
    #    except:
    #         print('error')
