from urllib import request,parse
url='http://httpbin.org/post'
headers={
    'User-Agent':'Mozilla/4.0(compatible;MSIE 5dfgdfg.5;Windows NT)',
    'Host':'httpbin.org'
}
dict={
    'name':'myfish'
}

data= bytes(parse.urlencode(dict),encoding='UTF-8')
req = request.Request(url,data=data,headers=headers,method='POST')
response= request.urlopen(req)
print(response.read().decode('UTF-8'))
print('text github')



