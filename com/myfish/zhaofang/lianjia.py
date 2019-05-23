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
import time


LOG = "D:\zhaofang\log.txt"

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
location = {"andingmen","anzhen1","aolinpikegongyuan11","dongzhimen",
            "gongti","guozhan1","hepingli","huixinxijie","madian1",
            "sanlitun","sanyuanqiao","shaoyaoju","taiyanggong","xibahe","yayuncun",
            "yayuncunxiaoying","wangjing"}
district_list=("dongcheng","xicheng","chaoyang","haidian","fengtai")

zizhu_=("anzhen1","hepingli","xibahe","guozhan1","huixinxijie","taiyanggong","shaoyaoju","yayuncun", "yayuncunxiaoying")
gaishan_=("aolinpikegongyuan11","wangjing","beiyuan2","nanshatan1")

# xuequ_=("madian1","anzhen1",'dongzhimen','jiaodaokou','dongsi1','liupukang','deshengmen','xuanwumen12','andingmen')
dewaixuequ_=("madian1",'liupukang','deshengmen')

not_xicheng_list=("北环中心","德胜凯旋","月季园","德胜置业","鼓楼外大街",
                  "裕民路4号院","裕民路3号院","黄寺后身36号院","冠城南园",
                  "裕民路1号院","北三环中路43号院","裕民东里","七省办",
                  "北太平庄路2号院","马甸西路","京友公寓","玉兰园",
                  "钟表北园","中航宿舍","冠城北园","电信宿舍")


# 筛选区县还是区域
DIS_LIST = dewaixuequ_
EXCEL_NAME = 'dewaixuequ_'
current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
house_number = 0
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


first_url = 'https://bj.lianjia.com/ershoufang/'
middle_url = "/pg"
last_url = '/bp100ep1300ba10ea30000s/'

mylist = []
database =[]
date1=''
date2=''

def house_info(dis,i):
    global count
    single_count = 0

    page_url = str(i+1)
    # 列表页url 域名+区域+中间url+页码+后缀url筛选条件
    # https://bj.lianjia.com/ershoufang/haidian/pg1/bp500ep1200ba70ea20000l2l3l4l5sf1f2f5ie2/
    detail_url = first_url+dis+middle_url+page_url+last_url

    print(detail_url)
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    #browser = webdriver.Chrome()
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(detail_url)

    #print(browser.page_source)
    list =browser.find_element_by_class_name('sellListContent').find_elements_by_css_selector('.clear.LOGCLICKDATA ')
    for item in list:
        score=0

        try:
            url = item.find_element_by_class_name('noresultRecommend').get_attribute('href')
        except:
            url='https://bj.lianjia.com/ershoufang/10110xxxxxxx.html'
        try:
            id = item.find_element_by_tag_name('a').get_attribute('data-housecode')
            id = "lj"+id
        except:
            id="lj"+url[34:-5]
        title = item.find_element_by_class_name('title').find_element_by_tag_name('a').text.strip()
        info1 = item.find_element_by_class_name('address').find_element_by_class_name('houseInfo').text.strip()
        a = info1.find("/")
        b = info1.find("/",a+1)
        c = info1.find("/",b+1)
        d = info1.find("/",c+1)
        e = info1.find("/",d+1)
        forbidden = ''

        xiaoqu = info1[:a].strip()






        huxing = info1[a+1:b].strip()
        mianji =info1[b+1:c-2].strip()
        chaoxiang=info1[c+1:d].strip()
        zhuangxiu=info1[d+1:e].strip()
        dianti=info1[e+1:].strip()

        info2 = item.find_element_by_class_name('flood').find_element_by_class_name('positionInfo').text.strip()
        f=info2.find("/")
        g=info2.find("/",f+1)
        h=info2.find("(")

        louceng=info2[:h].strip()
        zonggao=info2[h+1:f-1].strip()

        niandai=info2[f+1:f+5].strip()

        louxing=info2[f+7:g].strip()
        diqu = info2[g+1:].strip()
        guandai = item.find_element_by_class_name('followInfo').text.strip()

        i = guandai.find("/")
        j = guandai.find("\n")
        guanzhu=guandai[:i-3]
        daikan =guandai[i+1:j-3]

        try:
            ditie =item.find_element_by_class_name('subway').text.strip()
        except:
            ditie = ''
        try:
            VR=item.find_element_by_class_name('vr').text.strip()
        except:
            VR = ''
        try:
            taxfree=item.find_element_by_class_name('taxfree').text.strip()
            taxfree = '5年'
        except:
            try:
                taxfree=item.find_element_by_class_name('five').text.strip()
                taxfree='2年'
            except:
                taxfree='不满'
        try:
            kanfang=item.find_element_by_class_name('haskey').text.strip()
        except:
            kanfang = ''
        zongjia=item.find_element_by_class_name('totalPrice').text.strip()[:-1]
        danjia=item.find_element_by_class_name('unitPrice').text.strip()[2:-4]

        if   diqu== '和平里':   diqu_score = 10 * diqu_rate


        elif diqu == '马甸':  diqu_score = 10 * diqu_rate
        elif diqu == '六铺炕':  diqu_score = 8 * diqu_rate
        elif diqu == '德胜门':  diqu_score = 8 * diqu_rate

        else :                  diqu_score = 1 * diqu_rate

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

        chaoxiang = chaoxiang.replace(' ', '')
        cxset = set(chaoxiang)
        chaoxiang = ''.join(cxset)

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

        elif chaoxiang =='东西北' or chaoxiang =='西北东':
            chaoxiang='东西北'
            chaoxiang_score=6*chaoxiang_rate

        elif chaoxiang =='南西东' or chaoxiang =='东南西':
            chaoxiang='东西南'
            chaoxiang_score=7*chaoxiang_rate



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

        if louceng == '顶层' and (total_building == 6 or total_building == 7 or total_building == 5):
            louceng_score = 3 * louceng_rate
        elif louceng == '高楼层' and (total_building == 6 or total_building == 7 or total_building == 5):
            louceng_score = 5 * louceng_rate
        elif louceng == '中楼层' and (total_building == 6 or total_building == 7 or total_building == 5):
            louceng_score = 8 * louceng_rate

        elif louceng == '低楼层' and (total_building == 6 or total_building == 7 or total_building == 5):
            louceng_score = 10 * louceng_rate
        elif louceng == '底层' and (total_building == 6 or total_building == 7 or total_building == 5):
            louceng_score = 8 * louceng_rate
        elif louceng == '低楼层':
            louceng_score = 7 * louceng_rate
        elif louceng == '中楼层':
            louceng_score = 8 * louceng_rate
        elif louceng == '高楼层':
            louceng_score = 10 * louceng_rate
        elif louceng == '顶层':
            louceng_score = 9 * louceng_rate
        elif louceng == '底层':
            louceng_score = 6 * louceng_rate
        else:
            louceng_score = 2 * louceng_rate

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
                niandai_score = 1*niandai_rate
        except: niandai_score = 1*niandai_rate

        lou_score = louxing_score + louceng_score + niandai_score

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


        if louceng == '顶层' and (zonggao == '共7层' or zonggao == '共6层'):
            forbidden = '顶层'
        if float(mianji)<= 65:
            forbidden = '面积小'
        if int(niandai)<=1974:
            forbidden = '老楼'
        if xiaoqu in not_xicheng_list:
            forbidden = '外区'


        if id in get_log():
            flag = ''
        else:
            flag = '新房'
            save_log(id)
            print('========' + diqu + '========' + str(count) + '========' + str(house_number-single_count) + '========')
            print(' 链接 :' + url)
            # print(' ID :' + str(id))
            print(' 简介 :' + title,flag)
            # print(' 地区 :' + diqu)
            print(' 朝向 :' , chaoxiang, end='')
            print(' 户型 :' , huxing, end='')
            print(' 单价 :' + danjia)


        mylist.append([
                        id,score,rate_score,url, title, diqu, xiaoqu,
                        zongjia, danjia, huxing, mianji, chaoxiang, zhuangxiu,
                        dianti, louceng,zonggao, niandai, louxing,
                        ditie, VR, taxfree, kanfang, guanzhu,daikan,fangwu_score,lou_score,fujia_score,forbidden,flag])

        count=count+1
        single_count = single_count+1
    save_to_excel(dis,mylist)
    time.sleep(10)


def save_to_excel(dis,mylist):

    headers = (
    'ID','总分','性价比','url', '标题', '地区',  '小区',
    '总价', '单价','户型', '面积', '朝向', '装修',
    '电梯', '楼层','总楼层', '年代', '楼型',
    '地铁', 'VR', '满五', '看房', '关注量','带看量','房屋得分','楼得分','附加得分','无效','新房')
    #print(mylist)
    mylist = tablib.Dataset(*mylist, headers=headers)

    with open('D:\zhaofang\lianjia_'+EXCEL_NAME+current_time+'.xlsx', 'wb') as f:
        f.write(mylist.export('xlsx'))





def total_pages(url):

    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    # browser = webdriver.Chrome()
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(url)
    global house_number
    house_number = int(
        browser.find_element_by_class_name('resultDes').find_element_by_class_name('total').text[3:-9].strip())
    page_number= int(get_url(house_number))
    print('----共计'+str(house_number)+'套房屋----')
    print('----共计'+str(page_number)+'页----')
    return page_number



def get_url(next_page):
    if next_page<=30:
        return 1
    else :
        return int(next_page)/30+1

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

def main():
    loop_district()

if __name__ == "__main__":
    main()
