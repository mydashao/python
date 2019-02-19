num1 = 1

print(num1)

def add():
    global num1
    num1 = 100
    print(num1)

add()
print(num1)
