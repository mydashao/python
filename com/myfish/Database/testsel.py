import pymysql
id = 'tt0499549'
db = pymysql. connect( host ='localhost', user='root', password='777748', port=3306, db ='movie')
cursor = db. cursor()
sql = "SELECT ID FROM douban where IMDB='" + id + "'"
try:
    cursor.execute(sql)
    row = cursor. fetchone ()
    while row:
        print (row[0])

        row = cursor.fetchone()
except:
   print('Error ')