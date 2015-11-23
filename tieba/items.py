# -*- coding: utf-8 -*-
from scrapy import Item, Field

# 帖子列表中的帖子
class TiebaThreadItem(Item):
    thread_id = Field()         # 标题id
    tieba_id = Field()          # 贴吧id
    reply_num = Field()         # 回复数
    title = Field()             # 标题
    abstract = Field()          # 摘要
    url = Field()               # 帖子地址
    author = Field()            # 作者
    latest_replyer = Field()    # 最后回复者
    latest_reply_time = Field() # 最后回复时间

# 帖子中的回复
class TiebaPostItem(Item):
    post_id = Field()           # 回复id
    is_anonym = Field()         # 是否匿名
    thread_id = Field()         # 帖子id
    floor = Field()             # 楼层数
    content = Field()           # 回复内容
    comment_num = Field()       # 该回复的回复数（楼中楼）
    client = Field()            # 客户端
    reply_time = Field()        # 回复时间
    user_id = Field()           # 用户id
    user_name = Field()         # 用户名（若is_anonym=1，则为用户ip）