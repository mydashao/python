def money_to_int(string):
    money =string.replace(',','')
    if money[0] == '￥':
        return int(int(money[1:])/7)
    elif money[0] == '£':
        return int((int(money[1:])*1.3))



string = '￥2,788,243,800'
string2 = '£2,788,243,800'
print(money_to_int(string))
print(money_to_int(string2))