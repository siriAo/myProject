# _*_ coding : utf-8 _*_
# @Time : 2022-09-19 16:43
# @Author : Ao_Jiao
# @File : search_by_topic
# @Project : myProject
# 问题:话题搜索有投票环节，考虑在老版本上兼容进行
TOPIC = '为什么不建议学龄前儿童自己刷牙'
SEARCH_URL = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26t%3D10%26q%3D%23{}%23&page_type=searchall'.format(
    TOPIC)
