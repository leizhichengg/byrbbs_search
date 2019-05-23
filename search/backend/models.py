from django.db import models
from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

connections.create_connection(hosts=["localhost"])

# Create your models here.

class ByrArticleIndex(Document):
    suggest = Completion(analyzer="ik_analyzer")
    top_section_name = Text(analyzer="ik_max_word")
    section_name = Text(analyzer="ik_max_word")
    article_title = Text(analyzer="ik_max_word")
    article_url = Keyword()
    article_createtime = Text()
    article_author = Text(analyzer="ik_max_word")
    article_content = Text(analyzer="ik_max_word")
    article_comment = Integer()

    class Index:
        name = 'byrbbs'