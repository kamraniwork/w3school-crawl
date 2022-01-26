# Scraping W3School.com and Search it with elastic search 

1. [Scrap](#scrap)
2. [Search](#search)
## scrap
we can use the following command for scrap `w3school.com` site
and save object in file into `dataset/p.json`

```
scrapy crawl w3school -o dataset/p.json
```
as a result:
```json
[
    {
      "name": "HTML", 
      "description": [
          {"tag_title": "<small>", 
           "tag_des": "HTML  TagExampleDefine a smaller text:More \"Try it Yourself\" examples below.Definition and UsageThe  tag defines smaller text (like \ncopyright and other side-comments). This tag is not deprecated, but it is possible to achieve richer \n(or the same) effect with CSS.Browser SupportGlobal AttributesThe  tag also supports the .Event AttributesThe  tag also supports the .More ExamplesExampleUse CSS to define smaller text:Related PagesHTML tutorial: HTML DOM reference: Default CSS SettingsMost browsers will display the  element with the following default values:Example"}
      ] 
    }
   ]
```
## search
first step in the following command, run elastic search and kibana with Docker:

run elastic search:
```
docker run --name elasticsearch_countainers --network elastic -p 9200:9200 -p 9300:9300 --env "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.6.2
```
run kibana:
```
docker run --name kibana2 --network elastic -p 5601:5601 --env "ELASTICSEARCH_HOSTS=http://elasticsearch_countainers:9200" docker.elastic.co/kibana/kibana:7.6.2
```
then must migrating index in elastic search:
```
python migrating.py
```
With the above command can all objects that there are in `dataset/p.json` put on elastic search

```python
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.connections import connections

class SearchElastic:
    def __init__(self, search=None):
        connections.create_connection()
        self._search = search
        self._Elastic = Search()

    def search(self):
        query = Q('query_string', query=self._search, fuzziness='AUTO')

        return self._Elastic.query(query).extra(size=100)

def show_obj_elastic(search):
    obj = SearchElastic(search=search)
    response = obj.search()
    res = response.execute()
    option = res.to_dict()
    result = [news for news in option['hits']['hits']]
    for i in result:
        print(i['_source']['title'])
        print(i['_source']['description'])
        print(str(i['_source']['id']) + ' with score ' + str(i['_score']))
        print("===========================================")

```
