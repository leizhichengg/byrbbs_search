from elasticsearch import Elasticsearch

client = Elasticsearch(hosts=["localhost"])

key_words = "mac"

page = 1

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
                }
            }
        )

print(response)