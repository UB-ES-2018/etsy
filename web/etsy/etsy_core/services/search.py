from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, InnerDoc, Nested
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from ..models import Product

connections.create_connection()


class Tag(InnerDoc):
    tags_name = Text()


class ProductIndex(DocType):
    name = Text()
    description = Text()
    shop_name = Text()
    owner_name = Text()
    tags = Text()

    class Meta:
        index = 'product-index'


def bulk_indexing():
    ProductIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing()
                             for b in Product.objects.all().iterator()))
