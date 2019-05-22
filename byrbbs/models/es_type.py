# -*- coding:utf-8 -*-

from elasticsearch_dsl import DocType,analyzer,Text,Keyword,Integer
from elasticsearch_dsl.connections import connections

# 建立连接
connections.create_connection(hosts="127.0.0.1")

class ArticleType(DocType):
    # 文章类型
    top_section_name = Text(analyzer="ik_max_word")
    section_name = Text(analyzer="ik_max_word")
    article_title = Text(analyzer="ik_max_word")
    article_url = Keyword()
    article_createtime = Text()
    url_object_id = Keyword()
    article_comment = Integer()
    article_author = Text(analyzer="ik_max_word")
    article_content = Text(analyzer="ik_max_word")

    class Meta:
        # 索引名称和文档名称
        index = "byrbbs"
        doc_type = "article"

if __name__ == '__main__':
    ArticleType.init()

