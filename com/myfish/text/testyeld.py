def countdown(n):
    while n > 0:
        yield n
        n -= 1


# 可以当迭代器来使用它
for x in countdown(10):
    print('T-minus', x)