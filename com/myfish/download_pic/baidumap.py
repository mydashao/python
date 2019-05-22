import requests
import os

def getTileByXYZ():
    z = 19  # 成都[[22568,22678],[6897,7009]]
    # xidx = [22568,22580]
    # yidx = [6897,6910]
    # xidx = [101212, 101232]
    # yidx = [37770,37794]
    xidx = [101212, 101222]
    yidx = [37770,37784]

    for y in range(yidx[0], yidx[1] + 1):
        for x in range(xidx[0], xidx[1] + 1):
            # url = "https://gss0.bdstatic.com/8bo_dTSlRcgBo1vgoIiO_jowehsv/tile/?qt=vtile&x={x}&y={y}&z=18&styles=pl&scaler=1&udt=20190518"
            url = "http://online3.map.bdimg.com/tile/?qt=tile&x={x}&y={y}&z=18&styles=pl" \
                  "&scaler=1&udt=20190518".format(x=x, y=y)
            download(url, x, y, z)
        print(y)

def download(url,x, y, z,title):
    folder_name = title
    file_name = url.split('/')[5]
    # print(file_name)
    print('\r', file_name, end='',flush=True)

    r = requests.get(url)
    path = "D:\\PanDownload\\PanData\\pic"+folder_name
    if os.path.exists(path) is False:
        os.makedirs(path)

    with open(path+'\\'+file_name, 'wb') as f:
        f.write(r.content)