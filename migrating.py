from elasticsearch_dsl.connections import connections
import index
import json

ES_CONNECTIONS = {
    'default': {
        'hosts': [
            {
                'host': 'localhost',
                'http_auth': '',
                'verify_certs': False,
                'port': '9200',
            }
        ]
    }
}


def migrate():
    index.my_index.delete(ignore=404)
    index.my_index.create()
    mapping = index.my_index.get_mapping()
    m_path = "mappings/mapping.json"
    with open(m_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=4)


def read_text_file(file_path):
    with open('dataset/' + file_path, 'r', encoding="utf8", errors="ignore") as f:
        lines = f.read()
        return lines


def add_to_elastic():
    connections.get_connection()
    try:
        f = open('dataset/p.json')
        data = json.load(f)
        count = -1
        for i in data:
            count += 1
            print(count)
            tag_obj = index.Tag(
                tag_title=i['description'][0]['tag_title'],
                tag_des=i['description'][0]['tag_des']
            )
            w3_obj = index.W3learn(
                id=count,
                title=i['name'],
                description=tag_obj
            )
            w3_obj.save()

    except Exception as e:
        print(e)


def main():
    connections.create_connection()
    migrate()
    add_to_elastic()


main()
