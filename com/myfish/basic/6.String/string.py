spam= 'Hello world!'
print(id(spam))
print(spam[4])
print(spam[:5])
print(id(spam))

spam=spam[:5]
print(id(spam))
spam = 'SpamSpamBaconSpamEggsSpamSpam'
spam = spam.strip('SpamsgBacon')
print(spam)