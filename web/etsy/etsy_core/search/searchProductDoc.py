from elasticsearch_dsl import Document, Text, Date, InnerDoc, Nested


class ProductIndex(Document):
    name = Text()
    description = Text()
    shop_name = Text()
    owner_name = Text()
    tags = Text()

    class Index:
        name = 'product-index'
