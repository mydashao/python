from urllib import request,error
try:
    response = request.urlopen('https://docs.python.org/9.9')
except error.HTTPError as e:
    print(e.reason,e.code,e.headers,sep='\n')
except error.URLError as e:
    print(e.reason)
else:
    print('OK')