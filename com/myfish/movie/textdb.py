import pymysql

def get_douban_id(id):
    db = pymysql.connect(host='localhost', user='root', password='777748', port=3306, db='movie')
    cursor = db.cursor()
    sql = "SELECT ID,AKA FROM douban where IMDB_id='"+id+"'"
    print(sql)
    try:
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
           aka = str(data[1])
           citle = str(data[2])
           if aka != None:
               return aka
           else:
               return citle
        else :
            return ''

    except Exception as e:
        print(e)
        return '00000000'

print(get_douban_id('tt0338562'))