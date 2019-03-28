import time,datetime
int  = 1553285246
timeArray = time.localtime(int)#1970秒数
cookie_time= time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
current_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
print((int-time.time())//3600)
print((int-time.time())%3600//60)


print(current_time)
print(cookie_time)




