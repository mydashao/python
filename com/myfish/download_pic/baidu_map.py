import requests
import os
from PIL import Image
import time


'''
chengdu:
左下角：103.801536,30.389814
右上角：104.299382,30.836448
http://online3.map.bdimg.com/tile/?qt=tile&x=22568&y=6898&z=17&styles=pl&scaler=1&udt=20180601
http://online4.map.bdimg.com/tile/?qt=tile&x=22676&y=7008&z=17&styles=pl&scaler=1&udt=20180601
https://gss0.bdstatic.com/8bo_dTSlRcgBo1vgoIiO_jowehsv/tile/?qt=vtile&x=50605&y=18872&z=18&styles=pl&scaler=1&udt=20190518
https://gss0.bdstatic.com/8bo_dTSlRcgBo1vgoIiO_jowehsv/tile/?qt=vtile&x=50617&y=18885&z=18&styles=pl&scaler=1&udt=20190518
'''

path = "D:\\picc"


def savePngByXYZ(url, x, y,z,title):

    r = requests.get(url)
    sname = "D:/选区模型/cd_{y}_{x}.png".format(x=x, y=y)
    file_name = title
    # print(file_name)

    r = requests.get(url)
    path = "D:\\picc"
    if os.path.exists(path) is False:
        os.makedirs(path)

    with open(path+'\\'+file_name, 'wb') as f:
        f.write(r.content)


def getTileByXYZ():

    z = 19  # 成都[[22568,22678],[6897,7009]]
    # xidx = [22568,22580]
    # yidx = [6897,6910]
    xidx = [101233, 101234]
    yidx = [37742,37772]
    countx = xidx[1] - xidx[0]+1
    county = yidx[1] - yidx[0]+1
    print(countx,county)
    # xidx = [101212, 101222]
    # yidx = [37770,37784]

    for y in range(yidx[0], yidx[1] + 1):
        for x in range(xidx[0], xidx[1] + 1):
            title = 'DW_'+str(y)+'_'+str(x)+".jpg"
            # url = "https://gss0.bdstatic.com/8bo_dTSlRcgBo1vgoIiO_jowehsv/tile/?qt=vtile&x={x}&y={y}&z=18&styles=pl&scaler=1&udt=20190518"
            url = "http://online3.map.bdimg.com/tile/?qt=tile&x={x}&y={y}&z=19&styles=pl" \
                  "&scaler=1&udt=20190518".format(x=x, y=y)
            savePngByXYZ(url, x, y, 19,title)
            print(x,'*',y)
        time.sleep(0)

    merge(countx,county)



# import pyautogui
# import re
'''
把当前目录下的10*10张jpeg格式图片拼接成一张大图片
'''

def merge(countx,county):
    # 图片压缩后的大小
    width_i = 256
    height_i = 256

    # 每行每列显示图片数量
    line_max = countx
    row_max = county

    # 参数初始化
    all_path = []
    num = 0
    pic_max = line_max * row_max


    for root, dirs, files in os.walk(path):
        for file in files:
            if "jpg" in file:
                all_path.append(os.path.join(root, file))

    toImage = Image.new('RGBA', (width_i * line_max ,height_i * row_max))
    print('分辨率',width_i * line_max,'*',height_i * row_max)
    for i in range(0, row_max):

        for j in range(0, line_max):
            pic_fole_head = Image.open(all_path[num])
            width, height = pic_fole_head.size

            tmppic = pic_fole_head.resize((width_i, height_i))

            loc = (int(j  * height_i),int((row_max - i-1 )* width_i))

            # print("第" + str(num) + "存放位置" + str(loc))
            toImage.paste(tmppic, loc)
            num = num + 1
            # toImage.save('D:\\picc\\merged.png')

            if num >= len(all_path):
                print("breadk")
                break

        if num >= pic_max:
            break

    print(toImage.size)
    toImage.save('D:\\picc\\merged.png')
    print('瓦片拼接完毕')



if __name__ == "__main__":
    getTileByXYZ()
    print('瓦片下载完毕')