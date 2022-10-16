# _*_ coding : utf-8 _*_
# @Time : 2022-10-11 19:45
# @Author : Ao_Jiao
# @File : user
# @Project : myProject
class User:
    def __init__(self, screen_name, id, followers_count):
        self.screen_name = screen_name
        self.id = id
        self.followers_count = followers_count

    def toMongo(self) -> dict:
        return {'screen_name': self.screen_name,
                'id': self.id,
                'followers_count': self.followers_count}
