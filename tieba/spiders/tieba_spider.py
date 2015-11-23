# -*- coding: utf-8 -*-
import json
import datetime

from scrapy import Spider, Request
from scrapy import log
from tieba.items import TiebaThreadItem
from tieba.items import TiebaPostItem

import yaml

class TiebaSpider(Spider):
    # 'scrapy crawl' + name
    name = 'tieba'
    # 允许访问的domains
    allow_domains = ['http://tieba.baidu.com/']

    #加载配置
    def __init__(self):
        CONFIG = yaml.load(open('config.yaml'))

        self.tieba_url = CONFIG['tieba']['url']
        self.tieba_id = CONFIG['tieba']['id']
        self.end_page = CONFIG['page']

    # 类运行入口
    def start_requests(self):
        for pn in range(self.end_page):
            # 对每页进行请求，并将response交给parse_thread_item处理
            yield Request(self.tieba_url + '&pn=' +str(pn*50), 
                callback=self.parse_thread_item, 
                meta={'tieba_id': self.tieba_id},
                priority=10)

    # 解析thread对象（即帖子列表中展示的每个帖子）
    def parse_thread_item(self, response):
        articles = response.css('li.j_thread_list')
        tieba_id = response.meta['tieba_id']
        for article in articles:
            item = TiebaThreadItem()
            # 贴吧id
            item['tieba_id'] = tieba_id
            # 回复数
            r = article.css('span.threadlist_rep_num::text').extract()
            if r: item['reply_num'] = r[0]
            # 标题
            r  = article.css('a.j_th_tit::text').extract()
            if r: item['title'] = r[0]
            # 摘要
            r  = article.css('div.threadlist_abs_onlyline::text').extract()
            if r: item['abstract'] = r[0].strip()
            # 帖子地址
            r  = article.css('a.j_th_tit::attr(href)').extract()
            if not r: continue
            item['url'] = 'http://tieba.baidu.com'+r[0]
            item['thread_id'] = r[0][3:]
            # 作者
            r = article.css('span.tb_icon_author>a::text').extract()
            if r: item['author'] = r[0]
            # 最后回复者
            r = article.css('span.tb_icon_author_rely>a::text').extract()
            if r: item['latest_replyer'] = r[0]
            # 最后回复时间
            r = article.css('span.threadlist_reply_date::text').extract()
            if r: 
                t = r[0].strip()
                if ':' in t:
                    item['latest_reply_time'] = str(datetime.date.today())+' '+t
                elif '-' in t:
                    item['latest_reply_time'] = str(datetime.date.today().year)+'-'+t

            # 使用yield，否则循环将终止
            yield item
            # 对每个标题的url进行请求，并将response交给get_posts处理
            yield Request(item['url'], 
                    callback=self.get_posts, 
                    meta={'thread_id': item['thread_id']},
                    priority=20)

    # 获取每篇帖子的回复页数，分别请求
    def get_posts(self, response):
        # 帖子的回复页数
        page_count = response.css('span.red::text').extract()[-1]
        self.parse_post_item(response)

        for i in range(2, int(page_count)+1):
            # 对每页回复请求， response交给parse_post_item处理
            yield Request(response.url+'?pn='+str(i), 
                    callback=self.parse_post_item, 
                    meta={'thread_id': response.meta['thread_id'], 'pn': i},
                    priority=20)

    # 解析帖子中每个回复
    def parse_post_item(self, response):
        replys = response.css('div#j_p_postlist div.l_post')
        thread_id = response.meta['thread_id']
        pn = response.meta['pn']
        for reply in replys:
            data = json.loads(reply.css('::attr(data-field)').extract()[0])
            item = TiebaPostItem()
            # 回复id
            item['post_id'] = data['content']['post_id']
            # 是否匿名
            item['is_anonym'] = data['content']['is_anonym']
            # 帖子id
            item['thread_id'] = thread_id
            # 楼层数
            item['floor'] = data['content']['post_no']
            # 该回复的回复数（楼中楼）
            item['comment_num'] = data['content']['comment_num']
            if item['is_anonym'] != 1:
                # 用户id
                item['user_id'] = data['author']['user_id']
            # 用户名（若is_anonym=1，则为用户ip）
            item['user_name'] = data['author']['user_name']
            # 客户端
            r = reply.css('a.p_tail_wap::text').extract()
            if r: item['client'] = r[0].strip()
            # 回复内容
            try:
                item['content'] = data['content']['content']
            except:
                r = reply.css('div.d_post_content')
                if r: item['content'] = r[0].re(r'>(.*)</div')[0].strip()
            # 回复时间
            try:
                item['reply_time'] = data['content']['date']
            except:
                r  = reply.css('span.j_reply_data::text').extract()
                if r: item['reply_time'] = r[0].strip()

            yield item