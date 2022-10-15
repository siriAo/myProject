# _*_ coding : utf-8 _*_
# @Time : 2022-10-15 11:48
# @Author : Ao_Jiao
# @File : mongoDB
# @Project : myProject
from weiboSpider.asyn.item import Item
from motor.motor_asyncio import AsyncIOMotorClient


class Mongo:
    def __init__(self, *, connection_string=None, db: str, collection: str):
        if connection_string:
            self.client = AsyncIOMotorClient(connection_string)
        else:
            self.client = AsyncIOMotorClient()
        self.option = self.client[db][collection]
        # client = pymongo.MongoClient(host='localhost', port=207017)
        # client = pymongo.MongoClient('mongodb://localhost:27017/')

    async def insert_many(self, items: list[Item]):
        return await self.option.insert_many([item.toMongo() for item in items])
