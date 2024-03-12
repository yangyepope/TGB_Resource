from elasticsearch import Elasticsearch
import random
class soo:
    def getran(size):
        es = Elasticsearch("https://127.0.0.1:9200",
http_auth=("elastic","E4RH6kD28KESCNcpFBrf"),
verify_certs=False)
        body={
            'from':0,
            'query':{
                'match_all':{}
                }
        }
        a=es.count(index='video')
        num=a['count']
        a=es.search(index='video',body=body)
        print(a)
        b=random.randint(0, num)
        link=a['hits']['hits'][b]['_source']['link']
        title=a['hits']['hits'][b]['_source']['title']
        tag=a['hits']['hits'][b]['_source']['tag']
        return {
            'tag':tag,
            "title":title,
            'link':link
        }
    def write(title,tag,link):
        es = Elasticsearch("https://127.0.0.1:9200",
http_auth=("elastic","E4RH6kD28KESCNcpFBrf"),
verify_certs=False)
        es.index(index='video',document={
            'title':title,
            'tag':tag,
            'link':link
        })
    def so(key):
        es = Elasticsearch("https://127.0.0.1:9200",
http_auth=("elastic","E4RH6kD28KESCNcpFBrf"),
verify_certs=False)
        body = {
                
  "query":{

    "multi_match":{

      "query":str(key),

      "fields":["tag","title"]

    }

  },
    "sort":{
    "_script":{
        "script":"Math.random()",
        "type":"number",
        "order":"asc"
    }
}
                }
        se=es.search(index='video',body=body)
        total=se['hits']['total']['value']
        text="<b>一共搜索到{}条数据</b>\n".format(total)
        result=se['hits']['hits']
        id=1
        while not len(result)==0:
                    text+="\n{}.<a href='{}'>{}</a>".format(
                    id,
                    't.me/cnporn?start=g-'+str(result[0]['_source']['link']),
                    result[0]['_source']['title']
                )
                    id+=1
                    result.remove(result[0])
        return text

