# _*_ coding : utf-8 _*_
# @Time : 2022-11-08 20:24
# @Author : Ao_Jiao
# @File : mongoDB
# @Project : myProject
import pymongo
from item import Item


class Mongo:
    def __init__(self, *, connection_string=None, db: str, collection: str):
        if connection_string:
            self.client = pymongo.MongoClient(connection_string)
        else:
            self.client = pymongo.MongoClient()
        self.option = self.client[db][collection]

    def insert_many(self, items: [Item]):
        return self.option.insert_many([item.toMongo() for item in items])