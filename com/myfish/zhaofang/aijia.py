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

count=1
user_agent_list = [
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
# "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
# "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
# "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
# "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
# "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
# "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
]
zj1='500'
zj2='1200'
mj1='80'
mj2='200'
j3='l3'
j4='l4'
j5='l5'
location = {"andingmen","anzhen1","aolinpikegongyuan11","dongzhimen",
            "gongti","guozhan1","hepingli","huixinxijie","madian1","nanshatan1",
            "sanlitun","sanyuanqiao","shaoyaoju","taiyanggong","xibahe","yayuncun",
            "yayuncunxiaoying","wangjing"}
district_list={"dongcheng","xicheng","chaoyang","haidian","fengtai"}

district_list={"haidian"}

diqu_rate= 20

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

'''
l3l4l5 三四五居室
ie2有电梯 ie1没电梯
f朝向东南西北 f5南北朝向
lc 楼层 lc5顶层
url = 'bp'+zj1+'ep'+mj2+'ba'+mj1+'ea'+mj2+'l3l4l5hu0sf1lc2lc3lc5f5ie2'

'''

first_url = 'https://bj.5i5j.com/ershoufang/xichengqu/b500e1200f1f3f5h300l50r2r3r4r5r9n'



mylist = []
database =[]
date1=''
date2=''

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



    except:
        print('改变啦')
        script=html.head.script.text
        url = script[script.find("'", 1):-1].strip()
        print(soup)
        get_html(url)

    return soup

def house_info(dis,i):
    global count
    page_url = str(i+1)
    detail_url = first_url+page_url
    print(detail_url)

    soup = get_html(detail_url)

    url_list = soup.find('div', class_="list-con-box").find_all('li')

    for item in url_list:
        score=0
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
        ditie=info2[info2.rfind('·',1)+2:].strip()
        # print('地区：',diqu)
        # print('小区：',xiaoqu)
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
        # try:
        #     taxfree=item.find_element_by_class_name('taxfree').text.strip()
        #     taxfree = '5年'
        # except:
        #     try:
        #         taxfree=item.find_element_by_class_name('five').text.strip()
        #         taxfree='2年'
        #     except:
        #         taxfree='不满'



        if   diqu== '和平里':    diqu_score = 14 * diqu_rate
        elif diqu == '和平里':   diqu_score = 10 * diqu_rate
        elif diqu == '惠新西街':  diqu_score = 9 * diqu_rate
        elif diqu == '芍药居':   diqu_score = 8 * diqu_rate
        elif diqu == '亚运村': diqu_score = 8 * diqu_rate
        elif diqu == '国展': diqu_score = 8 * diqu_rate
        elif diqu == '亚运村小营': diqu_score = 8 * diqu_rate
        elif diqu == '西坝河': diqu_score = 8 * diqu_rate
        elif diqu == 'CBD': diqu_score = 7 * diqu_rate
        elif diqu == '太阳宫': diqu_score = 8 * diqu_rate
        elif diqu == '朝阳门外': diqu_score = 6 * diqu_rate
        elif diqu == '健翔桥': diqu_score = 7 * diqu_rate
        elif diqu == '三元桥': diqu_score = 7 * diqu_rate
        elif diqu == '望京': diqu_score = 6 * diqu_rate
        elif diqu == '奥林匹克公园': diqu_score = 6 * diqu_rate
        elif diqu == '燕莎': diqu_score = 6 * diqu_rate
        elif diqu == '北苑': diqu_score = 5 * diqu_rate
        elif diqu == '大望路': diqu_score = 5 * diqu_rate
        elif diqu == '南沙滩': diqu_score = 5 * diqu_rate
        elif diqu == '农展馆': diqu_score = 5 * diqu_rate
        elif diqu == '四惠': diqu_score = 3 * diqu_rate
        elif diqu == '双井': diqu_score = 3 * diqu_rate
        elif diqu == '朝阳公园': diqu_score = 3 * diqu_rate
        elif diqu == '华威桥': diqu_score = 3 * diqu_rate
        elif diqu == '劲松':   diqu_score = 3 * diqu_rate
        elif diqu == '北工大': diqu_score = 3 * diqu_rate
        elif diqu == '立水桥': diqu_score = 3 * diqu_rate
        elif diqu == '潘家园': diqu_score = 3 * diqu_rate
        elif diqu == '酒仙桥': diqu_score = 3 * diqu_rate
        elif diqu == '红庙':   diqu_score = 3 * diqu_rate
        elif diqu == '十里河': diqu_score = 3 * diqu_rate
        elif diqu == '大山子': diqu_score = 2 * diqu_rate
        elif diqu == '十八里店': diqu_score = 2 * diqu_rate
        elif diqu == '双桥':  diqu_score = 1 * diqu_rate
        elif diqu == '朝青':  diqu_score = 1 * diqu_rate
        elif diqu == '东坝':  diqu_score = 1 * diqu_rate
        elif diqu == '常营':  diqu_score = 1 * diqu_rate
        elif diqu == '欢乐谷': diqu_score = 1 * diqu_rate
        elif diqu == '豆各庄': diqu_score = 1 * diqu_rate
        elif diqu == '石佛营': diqu_score = 1 * diqu_rate
        elif diqu == '百子湾': diqu_score = 1 * diqu_rate
        elif diqu == '甜水园': diqu_score = 2 * diqu_rate
        elif diqu == '十里堡': diqu_score = 1 * diqu_rate
        elif diqu == '成寿寺': diqu_score = 1 * diqu_rate
        elif diqu == '垡头':   diqu_score = 1 * diqu_rate
        elif diqu == '定福庄': diqu_score = 1 * diqu_rate
        elif diqu == '高碑店': diqu_score = 1 * diqu_rate
        elif diqu == '甘露园': diqu_score = 1 * diqu_rate
        elif diqu == '朝阳其它': diqu_score = 1 * diqu_rate
        else :                  diqu_score = 1 * diqu_rate

        if zhuangxiu == '5室3厅':
            huxing_score = 14 * huxing_rate
        elif chaoxiang == '5室2厅':
            huxing_score = 13 * huxing_rate
        elif chaoxiang == '5室1厅':
            huxing_score = 12 * huxing_rate
        elif chaoxiang == '4室3厅':
            huxing_score = 13 * huxing_rate
        elif chaoxiang == '4室2厅':
            huxing_score = 12 * huxing_rate
        elif chaoxiang == '4室1厅':
            huxing_score = 11 * huxing_rate
        elif chaoxiang == '3室3厅':
            huxing_score = 12 * huxing_rate
        elif chaoxiang == '3室2厅':
            huxing_score = 11 * huxing_rate
        elif chaoxiang == '3室1厅':
            huxing_score = 10 * huxing_rate
        elif chaoxiang == '3室0厅':
            huxing_score = 7 * huxing_rate
        elif chaoxiang == '2室2厅':
            huxing_score = 8 * huxing_rate
        elif chaoxiang == '2室1厅':
            huxing_score = 7 * huxing_rate
        elif chaoxiang == '2室0厅':
            huxing_score = 5 * huxing_rate
        else:
            huxing_score = 2 * huxing_rate






        if chaoxiang.replace(' ','')=='南北':      chaoxiang_score=10*chaoxiang_rate
        elif chaoxiang.replace(' ','')=='东南北':  chaoxiang_score=7*chaoxiang_rate
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
            if int(zonggao[1:-1]) >= 20:
                zonggao_score = 10*zonggao_rate
            elif int(zonggao[1:-1]) >= 15:
                zonggao_score = 8.5*zonggao_rate
            elif int(zonggao[1:-1]) >= 10:
                zonggao_score = 7*zonggao_rate
            else:
                zonggao_score = 5*zonggao_rate
        except: zonggao_score = 5*zonggao_rate

        if louceng == '高楼层':
            louceng_score = 10*louceng_rate
        elif louceng == '顶层':
            louceng_score = 9*louceng_rate
        elif louceng == '中楼层':
            louceng_score = 7*louceng_rate
            zonggao_score = 0.5*zonggao_score
        elif louceng == '低楼层':
            louceng_score = 4.5*louceng_rate
            zonggao_score = 0
        else:
            louceng_score = 2*louceng_rate
            zonggao_score = 0

        if louxing == '板楼':
            louxing_score = 10*louxing_rate
        elif louxing == '板塔结合':
            louxing_score = 8.5*louxing_rate
        else :
            louxing_score = 6.5*louxing_rate


        # 楼龄
        try:
            if int(niandai) >= 2010:
                niandai_score = 10*niandai_rate
            elif int(niandai) >= 2000:
                niandai_score = 8*niandai_rate
            elif int(niandai) >= 1990:
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
        # score =float('%.2f' %((fujia_score+fangwu_score+lou_score)/6))
        # rate_score = float('%.2f' % (score/int(danjia)*80000))
        score = 0
        rate_score =0
        print('=================' + dis + '===' + str(count) + '=================')
        print(' 链接 :' + url)
        print(' ID :' + str(id))
        print(' 简介 :' + title)
        print(' 地区 :' + diqu)
        # print(' 评分 :' , score, end='')
        # print(' 性价比 :' , rate_score, end='')
        print(' 总价 :' + zongjia)
        print(' 单价 :' + danjia)
        print(' 详情 :')
        print(' 小区 :' + xiaoqu)
        print(' 户型 :' + huxing)
        print(' 面积 :' + mianji)
        print(' 朝向 :' + chaoxiang)
        print(' 装修 :' + zhuangxiu)
        print(' 电梯 :' + dianti)
        print(' 楼层 :' + louceng)
        print(' 总高 :' + zonggao)
        #
        # print(' 年代 :' + niandai)
        # print(' 楼型 :' + louxing)
        print(' 地铁 :' + ditie)
        # print(' VR :' + VR)
        # print(' 购房 :' + taxfree)
        # print(' 看房 :' + kanfang)
        print(' 关注 :' + guanzhu)
        print(' 带看 :' + daikan)

        print(' 发布 :', fabu)






        mylist.append([id,score,rate_score,url, title, dis,diqu, xiaoqu, zongjia, danjia, huxing, mianji, chaoxiang, zhuangxiu,
    dianti, louceng,zonggao, niandai, louxing, ditie, VR, taxfree, fabu, guanzhu,daikan])

        count=count+1

    save_to_excel(dis,mylist)
    time.sleep(10)


def save_to_excel(dis,mylist):

    headers = (
    'ID','总分','性价比','url', '标题', '城区','地区',  '小区', '总价', '单价','户型', '面积', '朝向', '装修',
    '电梯', '楼层','总楼层', '年代', '楼型', '地铁', 'VR', '满五', '发布', '关注量','带看量')
    #print(mylist)

    mylist = tablib.Dataset(*mylist, headers=headers)

    with open('D:\zhaofang_AJ_'+dis+'.xlsx', 'wb') as f:
        f.write(mylist.export('xlsx'))

def save_to_database1():
    db = pymysql.connect(host='localhost', user='root', password='777748', port=3306, db='zhaofang')
    cursor = db.cursor()
    try:

        for i in range(3):
            sql = "INSERT INTO zhaofang " \
                  "(id,score,rate_score,url, title, " \
                  "dis,diqu, xiaoqu, zongjia, danjia, " \
                  "huxing, mianji, chaoxiang, zhuangxiu,dianti, " \
                  "louceng,zonggao, niandai, louxing, " \
                  "ditie, VR, taxfree, kanfang, guanzhu,daikan) VALUES " \
                  "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE " \
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



def total_pages(url):
    soup = get_html(url)
    print('total_pages',soup)
    house_number = int(soup.find('div', class_="total-box").text[3:-3].strip())
    page_number= int(get_url(house_number))
    print('----共计'+str(house_number)+'套房屋----')
    print('----共计'+str(page_number)+'页----')
    return page_number



def get_url(next_page):
    if next_page<=30:
        return 1
    else :
        return int(next_page)/30+1

def main():
    for dis in district_list:
        district_first_url = first_url + '1'
        print("区域："+dis)
        total_page=total_pages(district_first_url)
        for i in range(total_page):

            house_info(dis,i)


if __name__ == "__main__":
    main()
