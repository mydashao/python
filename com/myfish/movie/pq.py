from pyquery import PyQuery as pq
import requests
url = 'http://www.w3school.com.cn/cssref/css_selectors.asp'
r = requests.get(url)
r.encoding = 'gb2312'
doc = pq(r.text)
print(doc('li'))