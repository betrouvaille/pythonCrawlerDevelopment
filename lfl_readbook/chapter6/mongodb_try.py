from pymongo import MongoClient

client = MongoClient()

db_name = 'Chapter6'
col_name = 'spider'
database = client[db_name]
collection = database[col_name]


# data = {'id': 12344, 'name': 'lfltest3', 'age': 19, 'salary': 190000}
# collection.insert_one(data)


print('全部返回', [x for x in collection.find()], '\n')
print('查询哪些记录age为19', [x for x in collection.find({'age': 19})], '\n')
print('只返回某些字段', [x for x in collection.find(
    {}, {'name': 1, 'salary': 1, '_id': 0})], '\n')


print('查询年纪>=18', [x for x in collection.find(
    {'age': {'$gte': 18}}, {'name': 1, 'salary': 1, 'age': 1, '_id': 0})], '\n')

print('按工资排序，显示名字和工资', [x for x in collection.find(
    {}, {'name': 1, 'salary': 1, "_id": 0}).sort('salary', -1)], '\n')


# 怎么 【更新】 MongoDB！！！！！

# collection.update_one({'age':20}, {'$set':{'name': 'kingname'}})  重置【第一个】年龄为20的人的名字为kingname
# collection.update_many({'age':20}, {'$set':{'age': 30}})  重置【所有】年龄为20的人的名字为kingname


# 怎么 【删除】 一些记录！！！！
# collection.delete_one({'name': 'kingname'}) 删除【第一个】叫kingname的人的记录
# collection.delete_many({'name': 'kingname'})  删除【所有】叫kingname的人的记录


# 怎么 【去重】！！
# collection.distinct('列名')
