# _*_ coding : utf-8 _*_
# @Time : 2022-10-12 11:35
# @Author : Ao_Jiao
# @File : mongoDBtest
# @Project : myProject
import pymongo

client = pymongo.MongoClient(host="localhost", port=207017)
client = pymongo.MongoClient('mongodb://localhost:27017/')
# 声明要操作的数据库
db = client.test
db = client['test']
# 声明要操作的集合
collection = db.students
collection = db['students']
student = {
    'id': '2020215119',
    'name': '焦奥'
}
student1 = {
    'id': 'simpleExample',
    'name': 'simple'
}
result = collection.insert_one(student)  # return InsertOneResult对象
result = collection.insert_many([student, student1])
print(result.inserted_ids)
# 不建议使用collection.insert
result = collection.insert(student)  # return MongoDB产生的ObjectId类型_id数值
result = collection.insert([student, student1])
