# _*_ coding : utf-8 _*_
# @Time : 2022-10-12 11:35
# @Author : Ao_Jiao
# @File : mongoDBtest
# @Project : myProject
import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient()
# client = pymongo.MongoClient(host='localhost', port=207017)
# client = pymongo.MongoClient('mongodb://localhost:27017/')

# 声明要操作的数据库
db = client.test
# db = client['test']

# 声明要操作的集合
collection = db.students
# collection = db['students']
student = {
    'id': '2020215119',
    'age': 21,
    'name': '焦奥',
    'testPoint': {'第一次测验': 100,
                  '第二次测验': 99,
                  '第三次测验': 98}
}
student1 = {
    'id': 'firstExample',
    'age': 22,
    'name': 'first',
    'testPoint': {'第一次测验': None}  # None在MongoDB中存为null
}
student2 = {
    'id': 'secondExample',
    'age': 23,
    'name': 'second',
    'testPoint': {'测验': [100, 99, 98]}
}

# 数据插入
result = collection.insert_one(student)  # return InsertOneResult对象
print(type(result), result)
print(result.inserted_id)
# <class 'pymongo.results.InsertOneResult'> <pymongo.results.InsertOneResult object at 0x000001E3FE1E9450>
# 6346822d57da8702e5809ffb

result = collection.insert_many([student1, student2])
print(type(result), result)
print(result.inserted_ids)
# <class 'pymongo.results.InsertManyResult'> <pymongo.results.InsertManyResult object at 0x000001E3FE1E99F0>
# [ObjectId('6346822d57da8702e5809ffc'), ObjectId('6346822d57da8702e5809ffd')]

# 不建议使用collection.insert
# result = collection.insert(student)  # return MongoDB产生的ObjectId类型_id数值
# result = collection.insert([student1, student2])


# 数据查询,没有匹配数据return None
# _id查询
x = collection.find_one({'_id': ObjectId('634671a934ac2bd4424d5459')})
print(type(x), x)
# <class 'NoneType'> None

# 条件查询
y = collection.find_one({'id': '2020215119'})
print(type(y), y)
# <class 'dict'> {'_id': ObjectId('634671a934ac2bd4424d5459'), 'id': '2020215119', 'name': '焦奥'}

q = collection.find({'age': {'$gt': 20}})  # age > 20
print(type(q), q)
for element in q:
    print(type(element), element)
# <class 'pymongo.cursor.Cursor'> <pymongo.cursor.Cursor object at 0x000001F1280C1D50>
# <class 'dict'> {'_id': ObjectId('63468d3c00c4b10276fcbb1f'), 'id': '2020215119', 'age': 21, 'name': '焦奥'}
# <class 'dict'> {'_id': ObjectId('63468d3c00c4b10276fcbb20'), 'id': 'firstExample', 'age': 22, 'name': 'first'}
# <class 'dict'> {'_id': ObjectId('63468d3c00c4b10276fcbb21'), 'id': 'secondExample', 'age': 23, 'name': 'second'}

# 正则查询
r = collection.find({'name': {'$regex': '.*?$Example'}})
print(type(r), r)
for element in r:
    print(type(element), element)
# <class 'pymongo.cursor.Cursor'> <pymongo.cursor.Cursor object at 0x000001F1280C25F0>

# 删除
# collection.delete_one({'name': '焦奥'})
# collection.delete_one({'name': 'firstExample'})
# collection.delete_one({'name': 'secondExample'})
# <class 'pymongo.results.DeleteResult'> 1 <pymongo.results.DeleteResult object at 0x000001E3FE1E9990>

o = collection.delete_many({'age': {'$gt': 20}})  # age>20
print(type(o), o.deleted_count, o)
# <class 'pymongo.results.DeleteResult'> 3 <pymongo.results.DeleteResult object at 0x000001F1280C2410>
