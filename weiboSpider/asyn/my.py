import re
from opencc import OpenCC
from random import Random

l = []
print(element for element in l)


def n():
    return []


print(n())

herf = 'https://m.weibo.cn/status/MaA5yCgXR?mblogid=MaA5yCgXR&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%9B%A0%E7%88%B8%E7%88%B8%E4%B8%8D%E8%AE%A9%E7%8E%A9%E5%A5%B3%E5%84%BF%E6%8A%BD%E6%B3%A3%E6%8E%A7%E8%AF%89%E5%8E%8B%E5%8A%9B%E5%A4%A7'
result = re.search('https://m\.weibo\.cn/status/(.*?)\?', herf)
print(result, result.group(1))

l = [1, 2, 3]
l.append(None)
print(l, len(l))

print(False == 0)
y = (1, 2)  # <class 'tuple'>
print(y[1])

context = '【直播：<a  href="https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E5%8F%B0%E9%A3%8E%E5%8D%97%E7%8E%9B%E9%83%BD%E6%88%96%E5%B0%86%E6%A8%AA%E6%89%AB%E6%97%A5%E6%9C%AC%23&extparam=%23%E5%8F%B0%E9%A3%8E%E5%8D%97%E7%8E%9B%E9%83%BD%E6%88%96%E5%B0%86%E6%A8%AA%E6%89%AB%E6%97%A5%E6%9C%AC%23&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%97%A5%E6%9C%AC%E5%8F%91%E5%B8%83%E6%9C%80%E9%AB%98%E7%BA%A7%E5%88%AB%E9%A2%84%E8%AD%A6" data-hide=""><span class="surl-text">#台风南玛都或将横扫日本#</span></a>】<a  href="https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E5%8F%B0%E9%A3%8E%E5%8D%97%E7%8E%9B%E9%83%BD%E5%AE%9E%E6%97%B6%E7%99%BB%E9%99%86%E8%B7%AF%E5%BE%84%23&extparam=%23%E5%8F%B0%E9%A3%8E%E5%8D%97%E7%8E%9B%E9%83%BD%E5%AE%9E%E6%97%B6%E7%99%BB%E9%99%86%E8%B7%AF%E5%BE%84%23&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%97%A5%E6%9C%AC%E5%8F%91%E5%B8%83%E6%9C%80%E9%AB%98%E7%BA%A7%E5%88%AB%E9%A2%84%E8%AD%A6" data-hide=""><span class="surl-text">#台风南玛都实时登陆路径#</span></a>中央气象台9月18日06时继续发布台风预报：今年第14号台风“南玛都”已于今天凌晨由超强台风级减弱为强台风级，其中心早上5点钟位于日本九州岛偏南方约445公里的西北太平洋洋面上，中心附近最大风力15级。此前，日本气象厅对九州地区鹿儿岛 ...<a href="/status/4815032129165154">全文</a>'
# ...<a href="/status/4815032129165154">全文</a>
result = re.search('<a href="(.*)">全文</a>', context)
print(result.group(1))
s = re.sub('<.*?>', '', context)
print(s)

pool = [1, 2, 3]
r = Random()  # 在pool中随机一个元素
print(r.choice(pool))

# for i in range(10):  # 0~9
#     print(i)

dic = {
    '0': '', '1': {3: ''}
}
print(len(dic))
print(dic)
for i in dic.items():
    print(i)
print(dic['1'])  # {3: ''}

try:
    print(dic[2])
    raise Exception
except Exception as e:
    print('异常信息{}'.format(e))
print('长度{}'.format(len(dic)))

# 中文utf-8编码范围为0X4E00-0x9FA5 即19968-40869
print('\u4E15')  # 丕
print(Random().randint(0, 2))  # 取值[a,b]

print(chr(555))  # 返回unicode编码对应字符
print(ord('🙏'), ord('，'))  # 返回unicode编码
print(ord('?'), ord('？'))

print(OpenCC('t2s').convert('怎么哪里都有你，不得不怀疑是否反串'))  # 简体中文转繁体

h = ''.strip()
print(h.strip() is None)
print(h)

# l = ['45~33的浓缩我冰本练一个能赌的胚子都没有你告诉我你是想让我退游吗？', ' ', '我想问问我神子1500的血被冰本里的那个冰丘丘人一屁股坐死了你是想让我给神子用生命杯生命沙生命头吗？', ' 芜湖冲', ' ',
#      '祝你拥有鼠标垫', ' ', ' ']
# l = ['抽', ' ', '好喜欢这种风格', ' 好牛逼', ' ', ' ', '逆天', ' ', '我玩的什么神仙游戏', '蹲一个']
l = ['', '给我来个风系不带帘子的散兵，谢谢', '回复', ':为什么会觉得很招黑？而且很多人都在下面发了对自己角色的一些看法，为什么其他人可以发加强我就不可以发我的意见呢友友', '回复', ':为啥呀，想吃瓜', '回复',
     ':？啊，怪我咯？', '阿桃什么时候复刻[开学季]', '回复', ':怎麼哪裏都有你，不得不懷疑是否反串', '回复', ':怎么招黑了？这不是角色单人向的微博吧，还是说你怕坏了所谓的路人缘', '回复',
     ':我不急等到散兵立绘出了就急不了了', '回复', ':我是真的会乐']

t = [x.strip() for x in l if x.strip() != '' and x != '回复']
o = [x.lstrip(':') for x in t if len(x) > 1]
print(o)
res = []
for x in o:
    m = re.sub(r'\[.*]', '', x)
    n = OpenCC('t2s').convert(m)
    res.append(n)
print(res)
# lambda argument_list: expression
lambda x=1, y=2: x * y  # 函数输入是x和y，输出是它们的积x * y

'''
filter(function or None, iterable)
fuction or None：第一个参数可以是一个函数或者是None,  iterable：可迭代对象
如果给了function，则将可迭代对象中的每一个元素，传递给function作为参数，筛选出所有结果为真的值。
如果function没有给出，必须要给None，直接返回iterable中所有为真的值
真值：任何非零的值（包括负数）
假值：零，所有的空（空列表等） None
0，False，所有的空
'''


# 过滤出列表中的所有奇数：
def is_odd(n):
    return n % 2 == 1


tmplist = filter(is_odd, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
newlist = list(tmplist)
print(newlist)
# 输出[1, 3, 5, 7, 9]

l = []
print(len(l))  # len(l)=0
print(l is None)  # False
