from elasticsearch_dsl import Document, Text, Date, InnerDoc, Nested, Float


class ProductIndex(Document):
    name = Text()
    description = Text()
    shop_name = Text()
    owner_name = Text()
    tags = Text()
    price = Float()

    class Index:
        name = 'product-index'
