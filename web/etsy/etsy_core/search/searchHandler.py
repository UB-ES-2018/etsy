from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search

from .. import models
from .searchProductDoc import ProductIndex


def create_elastic_connection():
    try:
        connections.get_connection().cluster.health()
    except:
        connections.create_connection(hosts=['elasticsearch:9200'])

    print(connections.get_connection().cluster.health())


def bulk_indexing():
    create_elastic_connection()
    ProductIndex.init()
    es = Elasticsearch(['elasticsearch:9200'])
    bulk(es, actions=(b.indexing()
                      for b in models.Product.objects.all().iterator()))


def search_item(query, page=1, pagesize=20):
    """
    Elasticsearch query for items. It returns a paginated amount of items that match a query.
    """
    create_elastic_connection()

    start = (page-1) * pagesize
    end = start + pagesize

    es = Elasticsearch(['elasticsearch:9200'])
    s = Search(index="product-index").using(es)
    s = s.query("simple_query_string", query=query,
                fields=["name^3", "description", "tags^4"])[start:end]

    results = []
    for hit in s:
        results.append(models.Product.objects.get(name=hit.name))

    paginator = Paginator(results, pagesize)

    try:
        items = paginator.get_page(page)
    except PageNotAnInteger:
        items = paginator.get_page(1)
    except EmptyPage:
        items = paginator.get_page(paginator.num_pages)

    return items
