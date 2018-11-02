from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, InnerDoc, Nested
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from .. import models
from searchProductDoc import ProductIndex

connections.create_connection()


def bulk_indexing():
    ProductIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing()
                             for b in models.Product.objects.all().iterator()))
