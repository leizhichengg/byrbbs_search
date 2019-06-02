# -*- coding: utf-8 -*-
import scrapy
import re
from byrbbs.items import ByrSectionItem
from byrbbs.spiders.byr_config import HEADERS,LOGIN_FORMDATA

class ByrSectionSpider(scrapy.Spider):
    pipeline = ['ByrSectionPipeline']
    name = "byr_section"
    allowed_domains = ["bbs.byr.cn"]
    pat = r'href=\"(.*?)\" title=\"(.*?)\"'
    section_pat = r'^/section/(.*?)$'
    start_urls = ['http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-0',
                  'http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-1',
                  'http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-2',
                  'http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-3',
                  'http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-4',
                  'http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-5',
                  'http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-6',
                  'http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-7',
                  'http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-8',
                  'http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-9'
                  ]
    top_section_name = ['本站站务','北邮校园','学术科技','信息社会','人文艺术',
                        '生活时尚','休闲时尚','体育健身','游戏对战','乡亲乡爱']

    def start_requests(self):
        return [scrapy.FormRequest("http://bbs.byr.cn/user/ajax_login.json",
                                   formdata=LOGIN_FORMDATA,
                                   meta={'cookiejar': 1},
                                   headers=HEADERS,
                                   callback=self.logged_in)]

    def logged_in(self, response):
        for url in self.start_urls:
            item = ByrSectionItem()
            num = int(url[-1])
            item['top_section_num'] = num + 1  # 使存储的类别号从1开始
            item['top_section_name'] = self.top_section_name[num]
            yield scrapy.Request(url, meta={'cookiejar': response.meta['cookiejar'],'item':item}, headers=HEADERS, callback=self.parse)

    def parse(self, response):
        top_section_num = response.meta['item']['top_section_num']
        top_section_name = response.meta['item']['top_section_name']
        body = response.body_as_unicode()
        data = body.replace(r'\"', '"') #原始形式为“/board/BTadvice\”，需删除尾部的\
        results = re.findall(self.pat, data, re.I)   #re,I 忽略大小写
        for result in results:
            url = result[0]
            title = result[1]
            rs = re.findall(self.section_pat, url, re.I)
            if rs:
                next_url = 'http://bbs.byr.cn/section/ajax_list.json?uid='+LOGIN_FORMDATA['id']+'&root=sec-%s' % rs[0]
                yield scrapy.Request(next_url, meta={'cookiejar': response.meta['cookiejar'],'item':response.meta['item']}, headers=HEADERS, callback=self.parse)
            else:
                item = ByrSectionItem()
                item['section_url'] = url
                item['section_name'] = title
                item['top_section_num'] = top_section_num
                item['top_section_name'] = top_section_name
                # yield item    #传出/存储于本地文件，用于测试
                yield scrapy.Request(response.urljoin(url), meta={'cookiejar': response.meta['cookiejar'], 'item': item}, headers=HEADERS,callback=self.parse_article_total)

    def parse_article_total(self,response):
        section_article_total = response.xpath('//*[@class="t-pre-bottom"]/div[1]/ul[1]/li[1]/i/text()').extract()
        item = response.meta['item']
        item['section_article_total'] = section_article_total[0]
        yield item