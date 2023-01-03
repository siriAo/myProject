# _*_ coding : utf-8 _*_
# @Time : 2023-01-03 15:15
# @Author : Ao_Jiao
# @File : scriptTest
# @Project : myProject
import pymongo
from bson.objectid import ObjectId

import Script.dataClean
# 使用配置
TextPath = ['text']
ArrayPath = ['topic']
# TextPath = ['submit_title', 'submit_content', 'reply_unit', 'reply_content']
# ArrayPath = []


def call(contents):
    print('数据清洗前 ' + contents)
    content = Script.dataClean.process(contents)
    print('数据清洗后 ' + content)
    return content


if __name__ == "__main__":
    client = pymongo.MongoClient()
    # 声明要操作的数据库
    db = client.weibo
    # 声明要操作的集合
    collection = db.title_data
    myCursor = collection.find()

    for doc in myCursor:

        for path in TextPath:
            contents = doc[path]
            if isinstance(contents, str):
                content = call(contents)
                collection.find_one_and_update({'_id': ObjectId(doc['_id'])}, {'$set': {path: content}})

        for path in ArrayPath:
            contents = doc[path]
            if isinstance(contents, list):
                for content in contents:
                    content = call(content)

    client.close()
