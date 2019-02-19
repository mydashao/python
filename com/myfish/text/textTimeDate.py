import time
import datetime

date ='14 Oct 2019'
date2 = '16 February 2018'
date_format=datetime.datetime.strptime(date,'%d %b %Y').strftime('%Y-%m-%d')
date2_format=datetime.datetime.strptime(date2,'%d %B %Y').strftime('%Y-%m-%d')

print(date_format)
print(date2_format)

print(date_format>date2_format)