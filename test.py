# _*_ coding : utf-8 _*_
# @Time : 2022-09-20 17:36
# @Author : Ao_Jiao
# @File : test
# @Project : myProject
import asyncio
import json
import requests
from pymongo.results import InsertManyResult

'''
headers = {'Host': 'cq.gov.cn',
           'Connection': 'keep-alive',
           'Content-Length': '62',
           'Pragma': 'no-cache',
           'Cache-Control': 'no-cache',
           'Accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
           'Content-Type': 'application/json',
           'Origin': 'http://www.cq.gov.cn',
           'Referer': 'http://www.cq.gov.cn/',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
           }
data = {"descend": True, "pageNo": 1, "pageSize": 30, "sort": "", "status": 2}
response = requests.post("http://cq.gov.cn/cq12345/api/bs-tsm-oworder-slave/page", headers=headers, json=data,
                         verify=False)
# 在报文中的数据形式{"descend": true, "pageNo": 1, "pageSize": 30, "sort": "", "status": 2}

response = requests.session().request('POST', "http://cq.gov.cn/cq12345/api/bs-tsm-oworder-slave/page", data=data)
# 在报文中的数据形式 descend=True&pageNo=1&pageSize=30&sort=&status=2
print(response.text)
'''

# 免费代理IP
'''
# {"code":1,"msg":"获取代理IP成功,IP代理池每5分钟更新一次,资源从各大免费代理网站中采集,获取到的随机可用代理IP都是由程序检测存活可连接代理!作者@LiuWa91",
# "proxyIp":"111.59.194.52:9091",
# "host":"111.59.194.52",
# "port":"9091",
# "area":"CN",
# "isChina":"true",
# "lastUpdateTime":"2022-09-22 14:20:04",
# "timeamp":1663836956818}
response = requests.get('https://cn.lwwangluo.store/cn')
js = json.loads(response.text)
proxy = js['proxyIp']
print(proxy)  # 223.68.190.136:9091
'''

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
