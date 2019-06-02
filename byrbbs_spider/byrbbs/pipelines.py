# -*- coding: utf-8 -*-
from byrbbs.spiders.byr_config import DB_CONFIG
import MySQLdb
import functools
from .models.es_type import ArticleType
# 去除html　tags
from w3lib.html import remove_tags
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

def check_pipline(func):
    @functools.wraps(func)
    def wrapper(self, item, spider):
        if self.__class__.__name__ in spider.pipeline:
            return func(self, item, spider)
        else:
            return item
    return wrapper

class ByrSectionPipeline(object):
    @check_pipline
    def process_item(self, item, spider):
        # 用spider.name区分不同的spier
        # https://segmentfault.com/q/1010000004863755
        con = MySQLdb.connect(**DB_CONFIG)
        cur = con.cursor()
        sql = 'insert into section(section_url,section_name,section_article_total,top_section_num,top_section_name) values(%s,%s,%s,%s,%s)'
        values = (item['section_url'], item['section_name'],item['section_article_total'],item['top_section_num'],item['top_section_name'])
        cur.execute(sql, values)  # second parameter must be iterabale
        con.commit()
        cur.close()
        con.close()
        return item

class ByrArticlePipeline(object):
    @check_pipline
    def process_item(self, item, spider):
        con = MySQLdb.connect(**DB_CONFIG)
        cur = con.cursor()
        sql = 'insert into articleinfo(section_name,article_title,article_url,article_comment,article_author,article_createtime) ' \
              'values(%s,%s,%s,%s,%s,%s)'
        values = (item['section_name'], item['article_title'], item['article_url'], item['article_comment'], item['article_author'], item['article_createtime'])
        cur.execute(sql, values)  # second parameter must be iterabale
        sql2 = 'insert into articlebody(article_url,article_content) values(%s,%s)'
        values2 = (item['article_url'],item['article_content'])
        cur.execute(sql2,values2)
        con.commit()
        cur.close()
        con.close()
        return item

class ElasticsearchPipeline(object):
    @check_pipline
    def process_item(self, item, spider):
        # 将item转换为ES的数据
        article = ArticleType()
        article.top_section_name = item['top_section_name']
        article.section_name = item['section_name']
        article.article_title = item['article_title']
        article.article_url = item['article_url']
        article.article_comment = item['article_comment']
        article.article_author = item['article_author']
        article.article_createtime = item['article_createtime']
        article.article_content = item['article_content']

        article.save()

        return item

