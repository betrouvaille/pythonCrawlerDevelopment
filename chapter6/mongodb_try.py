from pymongo import MongoClient

client = MongoClient()

db_name = 'Chapter6'
col_name = 'spider'
database = client[db_name]
collection = database[col_name]


# data = {'id': 12344, 'name': 'lfltest3', 'age': 19, 'salary': 190000}
# collection.insert_one(data)


print([x for x in collection.find()])
print([x for x in collection.find({'age': 19})])
