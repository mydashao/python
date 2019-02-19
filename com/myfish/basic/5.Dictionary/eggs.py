eggs=[1,2,3]
print(eggs)
print(id(eggs))
eggs=[4,5,6]
print(eggs)
print(id(eggs))

ducks = [1,2,3]
print(ducks)
print(id(ducks))
del ducks[2]
del ducks[1]
del ducks[0]
ducks.append(4)
ducks.append(5)
ducks.append(6)
print(ducks)
print(id(ducks))



