from ..items import BookItem

class BooksSpider(scrapy.Spider):

    def parse(self, response):
        for sel in response.css('article.product_pod'):
        book = BookItem()
        book['name'] = sel.xpath('./h3/a/@title').extract_first()
        book['price'] = sel.css('p.price_color::text').extract_first()
        yield book