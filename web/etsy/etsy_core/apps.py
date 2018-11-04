from django.apps import AppConfig
from elasticsearch_dsl.connections import connections


class EtsyCoreConfig(AppConfig):
    name = 'etsy_core'

    def ready(self):
        connections.create_connection(hosts=['elasticsearch:9200'])
        print(connections.get_connection().cluster.health())
        import etsy_core.signals
