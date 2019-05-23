from django.shortcuts import render
import json
from django.views.generic.base import View
# from search.backend.models import ByrArticleIndex
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from django.views.generic.base import RedirectView
from django.http import JsonResponse

client = Elasticsearch(hosts=["localhost"])

# Create your views here.

class IndexView(View):
    # 搜索排行榜
    pass


class SearchSuggestView(View):
    # 搜索建议
    pass


class SearchView(View):
    
    def get(request):
        # 获取搜索关键字
        key_words = request.GET.get("q", "")
        # key_words = "test"

        # 当前要获取第几页的数据
        page = request.GET.get("p", "1")
        # page = 1
        try:
            page = int(page)
        except BaseException:
            page = 1
        response = []
        response = client.search(
            index = "byrbbs",
            request_timeout=60,
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["article_title", "article_content"]
                    }
                },
                "from": (page - 1) * 20,
                "size": 20,
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "article_title": {},
                        "article_content": {},
                    }
                },
                "sort": [
                    { "article_createtime" : "desc" }
                ]
            }
        )

        hit_list = []

        for hit in response['hits']['hits']:
            hit_dict = {}
            try:
                if "article_title" in hit['highlight']:
                    hit_dict["article_title"] = "".join(hit["highlight"]["article_title"])
                else:
                    hit_dict["article_title"] = hit["_source"]["article_title"]
                if "article_content" in hit['highlight']:
                    hit_dict["article_content"] = "".join(hit["highlight"]["article_content"])
                else:
                    hit_dict["article_content"] = hit["_source"]["article_content"]
                hit_dict["article_createtime"] = hit["_source"]["article_createtime"]
                hit_dict["top_section_name"] = hit["_source"]["top_section_name"]
                hit_dict["section_name"] = hit["_source"]["section_name"]
                hit_dict["article_url"] = hit["_source"]["article_url"]
                hit_dict["article_comment"] = hit["_source"]["article_comment"]
                hit_dict["article_author"] = hit["_source"]["article_author"]
                hit_list.append(hit_dict)
            except:
                pass
            

            
        total_nums = int(response['hits']['total'])

        # 计算出总页数
        if (page % 20) > 0:
            page_nums = int(total_nums / 20) + 1
        else:
            page_nums = int(total_nums / 20)
        
        response = {}
        response['page'] = page
        response['all_hits'] = hit_list
        response['key_words'] = key_words
        response['total_nums'] = total_nums
        response['page_nums'] = page_nums

        return JsonResponse(response)


        # return render(request, "index.html", {"page": page,
        #                                        "all_hits": hit_list,
        #                                        "key_words": key_words,
        #                                        "total_nums": total_nums,
        #                                        "page_nums": page_nums,
        #                                        })
