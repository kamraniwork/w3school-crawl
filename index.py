from elasticsearch_dsl import (
    Document, Text, Index, Keyword, InnerDoc, Object
)
import analyze


class Tag(InnerDoc):
    tag_title = Text(analyzer=analyze.custom_filtering, )
    tag_des = Text(analyzer=analyze.custom_filtering,)


class W3learn(Document):
    id = Keyword()
    title = Text(analyzer=analyze.custom_filtering, )
    description = Object(Tag)

    class Index:
        name = 'w3'

    class Meta:
        doc_type = 'w3'

    def save(self, **kwargs):
        # self.created_at = datetime.now()
        return super(W3learn, self).save(**kwargs)

    def __repr__(self):
        return '<W3: {}>'.format(
            self.title,
        )


# create an index and register the doc types
my_index = Index('w3')
my_index.settings(number_of_shards=1, number_of_replicas=1)
my_index.document(W3learn)
