# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ByrArticleItem(scrapy.Item):
    # define the fields for your item here like:
    top_section_name = scrapy.Field()
    section_name = scrapy.Field()
    article_title = scrapy.Field()
    article_url = scrapy.Field()
    article_createtime = scrapy.Field()
    article_author = scrapy.Field()
    article_comment = scrapy.Field()
    article_content = scrapy.Field()

class ByrSectionItem(scrapy.Item):
    section_url = scrapy.Field()
    section_name = scrapy.Field()
    section_article_total = scrapy.Field()
    top_section_num = scrapy.Field()
    top_section_name = scrapy.Field()