import pymysql

db =pymysql.connect(host='localhost',user='root',password='777748',port=3306)
cursor=db.cursor()
cursor.execute('select version()')
data=cursor.fetchone()
print('database version:',data)
