# _*_ coding : utf-8 _*_
# @Time : 2022-10-15 11:48
# @Author : Ao_Jiao
# @File : mongoDB
# @Project : myProject
import logging
from weiboSpider.asyn.item import Item
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger()


class Mongo:
    def __init__(self, *, connection_string=None, db: str, collection: str):
        if connection_string:
            self.client = AsyncIOMotorClient(connection_string)
        else:
            self.client = AsyncIOMotorClient()
        self.option = self.client[db][collection]
        # client = pymongo.MongoClient(host='localhost', port=207017)
        # client = pymongo.MongoClient('mongodb://localhost:27017/')

    async def find_one(self, condition: dict):
        return await self.option.find_one(condition)

    async def insert_many(self, items: list[Item]):
        if len(items) != 0:
            # 筛选有效数据
            checked_items = [item.toMongo() for item in items if not await self.find_one({'bid': item.bid})]
            if len(checked_items) != 0:
                result = await self.option.insert_many(checked_items)
                logger.info('{} tips of data written in mongDB successfully'.format(len(result.inserted_ids)))
            else:
                logger.info('No new data needed to be written in MongoDB')
        else:
            logger.error('No data')
