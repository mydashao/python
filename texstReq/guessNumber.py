import random

sn= random.randint(1,100)

print('猜一个1-100的数字')

for times in range(1,8):
    print('猜吧')
    guess= int(input())

    if guess < sn:
        print('小了')
    elif guess > sn :
        print('大了')
    else:
        break

if guess ==sn and times>=5:
    print('猜对了，就是'+str(sn)+'，运气不好，猜了'+str(times)+'次')
elif guess ==sn and times<5:
    print('猜对了，就是'+str(sn)+'，运气很好，猜了'+str(times)+'次')
else:
    print('笨啊，是'+str(sn)+'啊')
