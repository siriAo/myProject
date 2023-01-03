# _*_ coding : utf-8 _*_
# @Time : 2022-09-20 17:36
# @Author : Ao_Jiao
# @File : test
# @Project : myProject
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

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
all_update = {
    'id': '2020215119',
    'age': 21,
    'name': '焦奥',
    'testPoint': {'第一次测验': 100,
                  '第二次测验': 100,
                  '第三次测验': 100}
}
part_update = {
    'testPoint': {'第一次测验': 100,
                  '第二次测验': 100,
                  '第三次测验': 100}
}


async def main():
    client = AsyncIOMotorClient()
    # 声明要操作的数据库
    db = client['test']
    # 声明要操作的集合
    collection = db['students']
    result = await collection.insert_many([student, student1, student2])
    print(type(result), result)
    print(len(result.inserted_ids), result.inserted_ids)
    # <class 'pymongo.results.InsertManyResult'> <pymongo.results.InsertManyResult object at 0x0000020DDEE41330>
    # 3 [ObjectId('634a7fa2ac432a604efcc24b'), ObjectId('634a7fa2ac432a604efcc24c'), ObjectId('634a7fa2ac432a604efcc24d')]

    i = await collection.find_one({'name': 'second'})
    print(type(i['testPoint']['测验']),i['testPoint']['测验'])
    # 抹除数据并更新全部字段
    i = await collection.find_one({'name': '焦奥'})
    print(i['testPoint'])
    i['testPoint'] = {'第一次测验': 100,
                      '第二次测验': 100,
                      '第三次测验': 100}
    result = await collection.update_one({'name': '焦奥'}, {'$set': i})
    print(result.matched_count, result.modified_count)
    # 仅更新dic中出现的字段
    i = await collection.find_one({'name': 'first'})
    print(i['testPoint'])
    i['testPoint'] = {'第一次测验': 100,
                      '第二次测验': 100,
                      '第三次测验': 100}
    result = await collection.update_one({'name': 'first'}, {'$set': part_update})
    print(result.matched_count, result.modified_count)

    await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
