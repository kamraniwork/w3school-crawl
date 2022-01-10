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
