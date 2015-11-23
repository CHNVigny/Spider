# -*- coding: utf-8 -*-

import json
import codecs

from scrapy import log

from tieba.items import TiebaThreadItem
from tieba.items import TiebaPostItem

# 对 TiebaThreadItem 对象进行保存
class JSONPipeline1(object):
    def __init__(self):
        self.file = codecs.open('items_thread.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, TiebaThreadItem):
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line.decode('unicode_escape'))

            info = 'thread_id %s' % (item['thread_id'])
            log.msg(info, level=log.INFO)
        return item

# 对 TiebaPostItem 对象进行保存
class JSONPipeline2(object):
    def __init__(self):
        self.file = codecs.open('items_post.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, TiebaPostItem):
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line.decode('unicode_escape'))

            info = 'post_id %s' % (item['post_id'])
            log.msg(info, level=log.INFO)
        return item

# class MySQLPipeline1(object):
#     def __init__(self):
#         CONFIG = yaml.load(open('config.yaml'))
#         self.con = MySQLdb.connect(CONFIG['db']['host'],
#                                    CONFIG['db']['user'],
#                                    CONFIG['db']['password'],
#                                    CONFIG['db']['database'],
#                                    charset='utf8')
#         self.cur = self.con.cursor()

#     def process_item(self, item, spider):
#         if isinstance(item, TiebaThreadItem):
#             info = 'thread_id %s' % (item['thread_id'])
#             try:
#                 sql = 'INSERT INTO threads (%s) VALUES (%s)' % (', '.join(item.keys()), ', '.join(['%(' + key + ')s' for key in item.keys()]))
#                 self.cur.execute(sql, dict(item))
#                 self.con.commit()
#                 log.msg('Save ' + info, level=log.INFO)
#             except MySQLdb.Error,e:
#                 sql = 'UPDATE threads SET %s WHERE thread_id=%s' % (', '.join([key + '=%(' + key + ')s' for key in item.keys()]), item['thread_id'])
#                 self.cur.execute(sql, dict(item))
#                 self.con.commit()
#                 log.msg('update ' + info, level=log.INFO)
#             except Exception as e:
#                 msg = ' '.join(['Error', info, str(e)])
#                 log.msg(msg, level=log.ERROR)
#         return item

# class MySQLPipeline2(object):
#     def __init__(self):
#         CONFIG = yaml.load(open('config.yaml'))
#         self.con = MySQLdb.connect(CONFIG['db']['host'],
#                                    CONFIG['db']['user'],
#                                    CONFIG['db']['password'],
#                                    CONFIG['db']['database'],
#                                    charset='utf8')
#         self.cur = self.con.cursor()

#     def process_item(self, item, spider):
#         if isinstance(item, TiebaPostItem):
#             info = 'post_id %s' % (item['post_id'])
#             try:
#                 sql = 'INSERT INTO posts (%s) VALUES (%s)' % (', '.join(item.keys()), ', '.join(['%(' + key + ')s' for key in item.keys()]))
#                 self.cur.execute(sql, dict(item))
#                 self.con.commit()
#                 log.msg('Save ' + info, level=log.INFO)
#             except MySQLdb.Error,e:
#                 sql = 'UPDATE posts SET %s WHERE post_id=%s' % (', '.join([key + '=%(' + key + ')s' for key in item.keys()]), item['post_id'])
#                 self.cur.execute(sql, dict(item))
#                 self.con.commit()
#                 log.msg('update ' + info, level=log.INFO)
#             except Exception as e:
#                 msg = ' '.join(['Error', info, str(e)])
#                 log.msg(msg, level=log.ERROR)
#         return item
#         