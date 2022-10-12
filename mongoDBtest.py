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
    'name': '焦奥'
}
student1 = {
    'id': 'firstExample',
    'age': 22,
    'name': 'first'
}
student2 = {
    'id': 'secondExample',
    'age': 23,
    'name': 'second'
}

# 数据插入
result = collection.insert_one(student)  # return InsertOneResult对象
print(type(result), result)
print(result.inserted_id)
# <class 'pymongo.results.InsertOneResult'> <pymongo.results.InsertOneResult object at 0x000001E3FE1E9450>


result = collection.insert_many([student1, student2])
print(type(result), result)
print(result.inserted_ids)
# <class 'pymongo.results.InsertManyResult'> <pymongo.results.InsertManyResult object at 0x000001E3FE1E99F0>

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
q = collection.find({'age': {'$gt': 20}})  # age>20
print(type(q), q)
# 正则查询
r = collection.find({'name': {'$regex': '.*Example'}})
print(type(r), r)

# 删除
# collection.delete_one({'name': '焦奥'})
# collection.delete_one({'name': 'firstExample'})
# collection.delete_one({'name': 'secondExample'})
# <class 'pymongo.results.DeleteResult'> 1 <pymongo.results.DeleteResult object at 0x000001E3FE1E9990>

o=collection.delete_many({'age': {'$gt': 20}}) # age>20
print(type(o), o.deleted_count, o)
