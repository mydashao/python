import time

print("倒计时程序")

for x in range(60,-1,-5):

    mystr = "倒计时" + str(x) + "秒"

    print(x,end = "")

    print(" " *1,end = "",flush=True)

    time.sleep(5)