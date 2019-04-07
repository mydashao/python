from scrapy import Item, Field
class BookItem(Item):
    name = Field()
    price = Field()