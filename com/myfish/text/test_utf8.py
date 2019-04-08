#coding=utf-8
from urllib.parse import quote
import string

url ='宇航员'.encode('GBK')
url = quote(url, safe=string.printable)  # safe表示可以忽略的字符
print(url)

