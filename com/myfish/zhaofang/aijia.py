'''
1. 根据url获取信息

'''

import random
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql

import tablib

LOG = "D:\zhaofang\AJlog.txt"

count=1
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
zj1='500'
zj2='1200'
mj1='80'
mj2='200'
j3='l3'
j4='l4'
j5='l5'

#
#
# zizhu_=("anzhen","hepingli","xibahe",
#              "guozhan","huixinxijie","sanyuanqiao","taiyanggong","shaoyaoju",
#             "yayuncun", "yayuncunxiaoying")
# gaishan_=("aolinpikegongyuan","wangjing","beiyuan","nanshatan1")
xuequ_=('madian','liupukang','deshengmen')
xuequ_=('deshengmen')

# 筛选区县还是区域
DIS_LIST = xuequ_
EXCEL_NAME = 'xuequ_'

diqu_rate= 10

chaoxiang_rate=10
huxing_rate=8
zhuangxiu_rate=7

louceng_rate=8
zonggao_rate=4
niandai_rate=6
louxing_rate=3.5

VR_rate=1
ditie_rate=6
kanfang_rate=1

taxfree_rate=5

first_url = 'https://bj.5i5j.com/ershoufang/'
last_url = '/b100e1300n'



mylist = []
database =[]
date1=''
date2=''
current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))

def get_html(url):

    headers = {'User-Agent': '', 'referer': 'link'}
    headers['User-Agent'] = random.choice(user_agent_list)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    try:
        title = soup.title.string
        print('没变：',title[0:40])
        # print(soup)
        timeout = 1
        while title[0:40]=='403 Forbidden':
            url =url[:-1]
            print(url)

            time.sleep(timeout*10)
            print('休眠',timeout*10,'秒')
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            title = soup.title.string
            timeout = timeout+1
            print(title[0:40])

        return soup
    except:
        print('改变啦')
        # print(soup)

        script=soup.html.head.script.text
        url = script[script.find("'", 1)+1:-2].strip()
        print(url)
        return get_html(url)


def house_info(dis,i):
    global count
    page_url = str(i+1)
    detail_url = first_url+dis+last_url+page_url
    print(detail_url)

    soup = get_html(detail_url)

    url_list = soup.find('div', class_="list-con-box").find_all('li')

    for item in url_list:
        url = item.find('div',class_='listImg').a.attrs['href']
        id = url[12:-5]
        url = 'https://bj.5i5j.com'+url

        id = "Aj"+id
        title = item.find('h3',class_='listTit').a.text.strip()
        # print('关注：','https://bj.5i5j.com'+url)
        # print('id：',id)
        # print('标题：',title)
        info1 = item.find('i',class_='i_01').find_parent('p').text.strip().replace(' ','')
        huxing = info1[0:info1.find('·', 1)].strip()
        mianji = info1[info1.find('·', 1)+1:info1.find('平米', 1)].strip()

        chaoxiang = info1[info1.find('平米')+3:info1.rfind('·',0,-8)].strip()
        louceng = info1[info1.rfind('·',0,-8)+1:info1.rfind('/')].strip()

        zonggao = info1[info1.rfind("/", 1)+1:info1.rfind("·", 1)].strip()
        zhuangxiu = info1[info1.rfind('·', 1)+1:].strip()

        # print('户型：',huxing)
        # print('面积：',mianji)
        # print('朝向：',chaoxiang)
        #
        # print('楼层：',louceng)
        # print('总高：',zonggao)
        # print('装修：',zhuangxiu)

        info2 = item.find('i',class_='i_02').find_parent('p').text.strip()

        diqu=info2[0:info2.find(' ',1)].strip()
        xiaoqu = info2[info2.find(' ',1):info2.rfind('·',1)].strip()
        xiaoqu = info2[info2.find(' ',1):].strip()

        ditie=info2[info2.rfind('·',1)+2:].strip()
        # print('地区：',diqu)
        # print('地铁：',ditie)

        info3 = item.find('i',class_='i_03').find_parent('p').text.strip()
        guanzhu=info3[0:info3.find(' ',1)].strip()
        daikan=info3[info3.find('带看',1)+2:info3.rfind('次',1)].strip()
        fabu=info3[info3.rfind('·',1)+2:-2].strip()
        # print('关注：',guanzhu)
        # print('带看：',daikan)
        # print('发布：',fabu)


        zongjia = item.find('p',class_='redC').find('strong').text.strip()
        danjiatt = item.find('div',class_='jia').text.replace(' ','').replace('\n','').strip()
        danjia = danjiatt[danjiatt.rfind('单价', 1)+2:-4]

        dianti=''
        niandai=''
        louxing=''
        VR = ''
        kanfang = ''
        taxfree=''

        if   diqu == '马甸': diqu_score = 10 * diqu_rate
        elif diqu == '六铺炕': diqu_score = 8 * diqu_rate
        elif diqu == '德胜门': diqu_score = 8 * diqu_rate

        else :diqu_score = 1 * diqu_rate

        if huxing == '5室3厅':
            huxing_score = 14 * huxing_rate
        elif huxing == '5室2厅':
            huxing_score = 13 * huxing_rate
        elif huxing == '5室1厅':
            huxing_score = 12 * huxing_rate
        elif huxing == '4室3厅':
            huxing_score = 13 * huxing_rate
        elif huxing == '4室2厅':
            huxing_score = 12 * huxing_rate
        elif huxing == '4室1厅':
            huxing_score = 11 * huxing_rate
        elif huxing == '3室3厅':
            huxing_score = 12 * huxing_rate
        elif huxing == '3室2厅':
            huxing_score = 11 * huxing_rate
        elif huxing == '3室1厅':
            huxing_score = 10 * huxing_rate
        elif huxing == '3室0厅':
            huxing_score = 7 * huxing_rate
        elif huxing == '2室2厅':
            huxing_score = 8 * huxing_rate
        elif huxing == '2室1厅':
            huxing_score = 7 * huxing_rate
        elif huxing == '2室0厅':
            huxing_score = 5 * huxing_rate
        else:
            huxing_score = 2 * huxing_rate

        chaoxiang = chaoxiang.replace(' ','')
        if chaoxiang =='南北':      chaoxiang_score=10*chaoxiang_rate

        elif chaoxiang =='东':  chaoxiang_score=5*chaoxiang_rate
        elif chaoxiang =='南':  chaoxiang_score=7*chaoxiang_rate
        elif chaoxiang =='西':  chaoxiang_score=3*chaoxiang_rate
        elif chaoxiang =='北':  chaoxiang_score=1*chaoxiang_rate

        elif chaoxiang =='东西':  chaoxiang_score=6*chaoxiang_rate

        elif chaoxiang == '东南' or chaoxiang =='南东':
            chaoxiang='东南'
            chaoxiang_score = 7 * chaoxiang_rate

        elif chaoxiang == '西南' or chaoxiang =='南西':
            chaoxiang='西南'
            chaoxiang_score = 6 * chaoxiang_rate

        elif chaoxiang =='南西北' or chaoxiang =='西南北':
            chaoxiang='西南北'
            chaoxiang_score=8*chaoxiang_rate

        elif chaoxiang =='南东北' or chaoxiang =='东南北':
            chaoxiang='东南北'
            chaoxiang_score=9*chaoxiang_rate

        elif chaoxiang =='东南西':  chaoxiang_score=7*chaoxiang_rate


        else: chaoxiang_score=4*huxing_rate

        if zhuangxiu == '精装':
            zhuangxiu_score= 10*zhuangxiu_rate
        elif chaoxiang == '其他':
            zhuangxiu_score = 6*zhuangxiu_rate
        elif chaoxiang == '简装':
            zhuangxiu_score = 6*zhuangxiu_rate
        else:
            zhuangxiu_score = 2*zhuangxiu_rate

        fangwu_score = chaoxiang_score+zhuangxiu_score+huxing_score

        try:
            total_building = int(zonggao[1:-1])

        except: total_building = 6

        if total_building>= 20:
            zonggao_score = 10 * zonggao_rate
        elif total_building >= 15:
            zonggao_score = 8.5 * zonggao_rate
        elif total_building >= 10:
            zonggao_score = 7 * zonggao_rate
        else:
            zonggao_score = 5 * zonggao_rate

        if louceng == '高楼层' and total_building ==6:
            louceng_score = 6*louceng_rate
        elif louceng == '顶层' and total_building == 6:
            louceng_score = 4 * louceng_rate
        elif louceng == '高楼层' and total_building ==7:
            louceng_score = 6*louceng_rate
        elif louceng == '顶层' and total_building ==7:
            louceng_score = 4*louceng_rate
        elif louceng == '中楼层' and total_building ==6:
            louceng_score = 6*louceng_rate
        elif louceng == '低楼层' and total_building ==6:
            louceng_score = 8 * louceng_rate
        elif louceng == '底层' and total_building ==6:
            louceng_score = 8*louceng_rate
        elif louceng == '低楼层':
            louceng_score = 6 * louceng_rate
        elif louceng == '中楼层':
            louceng_score = 8 * louceng_rate
        elif louceng == '高楼层':
            louceng_score = 10 * louceng_rate
        elif louceng == '顶层':
            louceng_score = 9 * louceng_rate
        elif louceng == '底层':
            louceng_score = 6 * louceng_rate
        else:
            louceng_score = 2*louceng_rate

        if louxing == '板楼':
            louxing_score = 10*louxing_rate
        elif louxing == '板塔结合':
            louxing_score = 8.5*louxing_rate
        else :
            louxing_score = 6.5*louxing_rate


        # 楼龄
        try:
            if int(niandai) >= 2000:
                niandai_score = 10*niandai_rate
            elif int(niandai) >= 1990:
                niandai_score = 8*niandai_rate
            elif int(niandai) >= 1980:
                niandai_score = 5*niandai_rate
            else:
                niandai_score = 3*niandai_rate
        except: niandai_score = 3*niandai_rate

        lou_score = louxing_score + louceng_score + niandai_score + zonggao_score

        # 近地铁，vr,随时看房
        if ditie=='近地铁':
            ditie_score = 10*ditie_rate
        else:
            ditie_score=0
        if VR == 'VR房源':
            VR_score = 10*VR_rate
        else:
            VR_score=0
        if kanfang == '随时看房':
            kanfang_score = 10*kanfang_rate
        else:
            kanfang_score=0

        # 满五唯一
        if taxfree=='5年':
            taxfree_score = 10*taxfree_rate
        elif taxfree == '2年':
            taxfree_score = 6*taxfree_rate
        else:
            taxfree_score = 2*taxfree_rate

        fujia_score = diqu_score+ditie_score+VR_score+kanfang_score+taxfree_score
        score =float('%.2f' %((fujia_score+fangwu_score+lou_score)/6))
        rate_score = float('%.2f' % (score/int(danjia)*80000))

        if id in get_log():
            flag = ''
        else:
            flag = '新房'
            save_log(id)
            print('=================' + dis + '===' + str(count) + '=================')
            print(' 链接 :' + url)
            print(' ID :' + str(id))
            print(' 简介 :' + title)
            #print(' 地区 :' + diqu)
            print(' 评分 :' , score, end='')
            print(' 性价比 :' , rate_score)
            # print(' 总价 :' + zongjia)
            # print(' 单价 :' + danjia)
            # print(' 详情 :')
            print(' 小区 :' + xiaoqu)


        mylist.append([id,score,rate_score,url, title, dis,diqu, xiaoqu, zongjia, danjia, huxing, mianji, chaoxiang, zhuangxiu,
    dianti, louceng,zonggao, niandai, louxing, ditie, VR, taxfree, fabu, guanzhu,daikan,flag])

        count=count+1

    save_to_excel(dis,mylist)
    time.sleep(30)


def save_to_excel(dis,mylist):

    headers = (
    'ID','总分','性价比','url', '标题', '城区','地区',  '小区', '总价', '单价','户型', '面积', '朝向', '装修',
    '电梯', '楼层','总楼层', '年代', '楼型', '地铁', 'VR', '满五', '发布', '关注量','带看量','新房')
    #print(mylist)

    mylist = tablib.Dataset(*mylist, headers=headers)

    with open('D:\AJ_'+EXCEL_NAME+current_time+'.xlsx', 'wb') as f:
        f.write(mylist.export('xlsx'))


def total_pages(url):
    soup = get_html(url)
    # print('total_pages',soup)
    print(url)

    house = soup.find('div', class_="total-box").text[0:-3].strip()
    lit = house.find('到')+1
    house_number = int(house[lit:].strip())
    page_number= int(get_url(house_number))
    print('----共计'+str(house_number)+'套房屋----')
    print('----共计'+str(page_number)+'页----')
    return page_number

# 保存日志
def save_log(id):
    # logger.debug('     开始保存cookie')

    with open(LOG, 'a+') as f:
        f.write(id+"\n")

# 读取日志
def get_log():
    result=[]
    # logger.debug('     开始读取cookie')
    with open(LOG, 'r') as f:
        for line in f:
            result.append(line.strip('\n'))
        return result


def loop_district():
    # 循环查询district_list中的各个区域
    for dis in DIS_LIST:
        district_first_url = first_url + dis + last_url
        print("区域："+dis)
        # 通过total_pages方法计算当前区域有多少个房源，多少页，返回总页数
        total_page=total_pages(district_first_url)
        # 循环查询每页信息
        for i in range(total_page):
            house_info(dis,i)


def get_url(next_page):
    if next_page<=30:
        return 1
    else :
        return int(next_page)/30+1

def main():
    for dis in DIS_LIST:
        district_first_url = first_url + dis + last_url
        print("区域："+dis)
        total_page=total_pages(district_first_url)
        for i in range(total_page):

            house_info(dis,i)

if __name__ == "__main__":
    main()
