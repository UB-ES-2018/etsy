from django.apps import AppConfig


class EtsyCoreConfig(AppConfig):
    name = 'etsy_core'

    def ready(self):
        import etsy_core.signals
