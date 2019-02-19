import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient(host='localhost',port=27017)

db= client.test
collection = db.students

student3={
    'id': '20170101',
    'name': 'Lebron',
    'age': 21,
    'gender':'male'
}
student4={
    'id': '20170101',
    'name': 'Curry',
    'age': 20,
    'gender':'male'
}

#result= collection.insert_many([student3,student4])
#print(result)

#findIverson = collection.find_one({'name':'Iverson'})
#print(findIverson)

results = collection.find({'age':20})
print(results)
for result in results:
    print(result)
