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

    async def write_in(self, items: [Item]):
        insert_arr = []
        if len(items) == 0:
            logger.error('No data to be written')
            return
        else:
            for item in items:
                old_item = await self.find_one({'bid': item.bid})
                if old_item:
                    await self.update_one(old_item, item)
                else:
                    insert_arr.append(item)
            if len(insert_arr) == 0:
                logger.warning('No new data needed to be written in MongoDB')
            else:
                await self.insert_many(insert_arr)
            return

    async def update_one(self, item, new_item):
        item['user'] = new_item.user.toMongo()
        item['comments_count'] = new_item.comments_count
        item['comments'] = new_item.commentstoMongo()
        try:
            await self.option.update_one({'bid': new_item.bid}, {'$set': item})
            logger.info('update data successfully whose bid={}'.format(new_item.bid))
        except Exception as e:
            logger.error('data update failed whose bid={}\n{}'.format(new_item.bid, e.message))

    async def find_one(self, condition: dict) -> dict or None:
        return await self.option.find_one(condition)

    async def insert_many(self, items: [Item]):
        try:
            result = await self.option.insert_many([item.toMongo() for item in items])
            logger.info('{} tips of data written in mongDB successfully'.format(len(result.inserted_ids)))
        except Exception as e:
            logger.error('insert failed\n{}'.format(e.message))
