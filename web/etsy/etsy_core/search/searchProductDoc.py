from elasticsearch_dsl import DocType, Text, Date, InnerDoc, Nested


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
